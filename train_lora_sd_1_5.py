import os
import torch
import numpy as np
import pandas as pd
import argparse
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import StableDiffusionImg2ImgPipeline, UNet2DConditionModel, AutoencoderKL
from safetensors.torch import save_file, load_file

# ✅ Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("--dataset_csv", type=str, default="/data/ephemeral/home/level4-cv-finalproject-hackathon-cv-05-lv3/dataset/dataset.csv")
parser.add_argument("--batch_size", type=int, default=4)
parser.add_argument("--epochs", type=int, default=10)
parser.add_argument("--lr", type=float, default=1e-4)
parser.add_argument("--output_dir", type=str, default="./lora_trained_model")
args = parser.parse_args()

device = "cuda" if torch.cuda.is_available() else "cpu"
df = pd.read_csv(args.dataset_csv).head(10)  # 상위 10개 샘플 사용

# ✅ 데이터셋 클래스 (검정색 이미지 필터링 포함)
class ImageDataset(Dataset):
    def __init__(self, dataframe):
        self.data = dataframe

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        source_path, target_path, prompt = row["source_image"], row["target_image"], row["generated_prompt"]

        source_image = Image.open(source_path).convert("RGB").resize((512, 512))
        target_image = Image.open(target_path).convert("RGB").resize((512, 512))

        np_source, np_target = np.array(source_image), np.array(target_image)

        if np.mean(np_source) < 5 or np.mean(np_target) < 5:  # 검정색 이미지 필터링
            print(f"⚠️ Skipping black image: {source_path} or {target_path}")
            return self.__getitem__((idx + 1) % len(self.data))

        return (
            torch.from_numpy(np_source).permute(2, 0, 1).float() / 255.0,
            torch.from_numpy(np_target).permute(2, 0, 1).float() / 255.0,
            prompt,
        )

# ✅ 데이터 로더 설정
dataloader = DataLoader(ImageDataset(df), batch_size=args.batch_size, shuffle=True)

# ✅ Stable Diffusion 모델 로드 (img2img)
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(device)
vae = AutoencoderKL.from_pretrained(model_id, subfolder="vae", torch_dtype=torch.float16).to(device)
unet = UNet2DConditionModel.from_pretrained(model_id, subfolder="unet", torch_dtype=torch.float16).to(device)
text_encoder = CLIPTextModel.from_pretrained(model_id, subfolder="text_encoder", torch_dtype=torch.float16).to(device)
tokenizer = CLIPTokenizer.from_pretrained(model_id, subfolder="tokenizer")

# ✅ Gradient Checkpointing 활성화 (메모리 절약)
unet.enable_gradient_checkpointing()
vae.enable_gradient_checkpointing()

# ✅ LoRA 가중치 적용
def apply_lora(unet, lora_path, alpha=1.0):
    print(f"✅ Applying LoRA weights from {lora_path}...")
    lora_weights = load_file(lora_path)
    for key, value in lora_weights.items():
        if "unet" in key and key in dict(unet.named_parameters()):
            dict(unet.named_parameters())[key].data.copy_(
                dict(unet.named_parameters())[key].data + alpha * value.to(device)
            )

# ✅ 옵티마이저 설정
optimizer = torch.optim.AdamW(unet.parameters(), lr=args.lr)

# ✅ 학습 루프
for epoch in range(args.epochs):
    for source_img, target_img, prompts in dataloader:
        optimizer.zero_grad()
        source_img, target_img = source_img.to(device), target_img.to(device)

        inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True).to(device)
        encoder_hidden_states = text_encoder(inputs["input_ids"]).last_hidden_state

        latents = vae.encode(source_img).latent_dist.sample().detach() * 0.18215
        target_latents = vae.encode(target_img).latent_dist.sample().detach() * 0.18215

        timesteps = torch.randint(0, 1000, (latents.shape[0],), dtype=torch.long, device=device)
        noise_pred = unet(latents, timesteps, encoder_hidden_states=encoder_hidden_states).sample

        loss = torch.nn.functional.mse_loss(noise_pred, target_latents)
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch+1}/{args.epochs}, Loss: {loss.item()}")

# ✅ LoRA 가중치 저장
os.makedirs(args.output_dir, exist_ok=True)
save_file({k: v.cpu() for k, v in unet.state_dict().items()}, f"{args.output_dir}/lora_trained.safetensors")

print("🎉 LoRA 학습 완료! 모델 저장됨:", args.output_dir)
