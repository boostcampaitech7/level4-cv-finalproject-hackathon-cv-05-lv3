import os
import torch
import open_clip
import pandas as pd
from PIL import Image
from torchvision import transforms
from diffusers import StableDiffusionImg2ImgPipeline
from safetensors.torch import load_file

def load_clip_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # 기존 코드에서는 model, preprocess 두 개만 받았는데, tokenizer까지 추가
    model, preprocess, tokenizer = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai")
    return model.to(device), preprocess, tokenizer, device

def apply_lora(pipe, lora_path, alpha=1.0):
    lora_weights = load_file(lora_path)
    for key, value in lora_weights.items():
        if "text_encoder" in key:
            layer = pipe.text_encoder
        elif "unet" in key:
            layer = pipe.unet
        else:
            continue
        layer_dict = dict(layer.named_parameters())
        if key in layer_dict:
            layer_dict[key].data += alpha * value.to(layer_dict[key].device)

def generate_prompt(image_path, model, preprocess, tokenizer, device):
    image = Image.open(image_path).convert("RGB")
    image = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)

    # 뱃지 스타일 프롬프트 후보
    text_candidates = [
        "a golden octagonal badge with intricate designs, highly detailed, embossed metal texture",
        "a futuristic neon glowing badge with a cyberpunk aesthetic, ultra-detailed, reflective",
        "a luxury platinum badge with precious gemstones embedded, elegant, high contrast",
        "a fantasy-style magical badge, radiating mystical energy, highly detailed, ornate patterns"
    ]

    # ✅ 수정된 부분: open_clip.tokenize() 사용
    text_tokens = open_clip.tokenize(text_candidates).to(device)

    with torch.no_grad():
        text_features = model.encode_text(text_tokens)

    similarity = (image_features @ text_features.T).softmax(dim=-1)
    best_prompt_idx = similarity.argmax().item()

    return text_candidates[best_prompt_idx]




def main():
    source_dir = "dataset/source_images"
    target_dir = "dataset/target_images"
    os.makedirs(target_dir, exist_ok=True)
    
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
    
    lora_models = [
        "badge.safetensors",
        "Badge_M.safetensors",
        "GameIconResearch_badge2_Lora.safetensors",
        "ingress_badge.safetensors"
    ]
    
    model, preprocess, tokenizer, device = load_clip_model()
    all_files = [f for f in os.listdir(source_dir) if f.endswith((".jpg", ".png", ".jpeg"))][:100]
    data = []
    
    for filename in all_files:
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        prompt = generate_prompt(source_path, model, preprocess, tokenizer, device)
        selected_lora = torch.choice(lora_models)
        apply_lora(pipe, selected_lora)
        
        init_image = Image.open(source_path).convert("RGB").resize((512, 512))
        
        generated_image = pipe(
            prompt=prompt,
            image=init_image,
            strength=0.8,
            guidance_scale=7.5,
            num_images_per_prompt=1
        ).images[0]
        
        generated_image.save(target_path)
        
        data.append([source_path, target_path, prompt, selected_lora, 0.8, 7.5])
    
    df = pd.DataFrame(data, columns=["source_image", "target_image", "prompt", "lora_model", "strength", "guidance_scale"])
    df.to_csv("dataset/dataset.csv", index=False)
    
    print("✅ dataset.csv 생성 완료! 책 표지 → 뱃지 변환 데이터셋 구축 완료 🎉")

if __name__ == "__main__":
    main()

