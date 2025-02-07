# badge_creator/badge_generator.py
import torch
from diffusers import StableDiffusionXLImg2ImgPipeline, DPMSolverMultistepScheduler
from PIL import Image

class SDXLBadgeGenerator:
    def __init__(
        self,
        base_model_id: str = "stabilityai/stable-diffusion-xl-base-1.0",
        lora_path: str = None,
        device: str = "cuda",
        torch_dtype=torch.float16,
    ):
        """
        SDXL Img2Img 파이프라인을 초기화합니다.
        
        :param base_model_id: SDXL 베이스 모델의 HuggingFace 모델 ID
        :param lora_path: LoRA 가중치 파일 경로 (옵션)
        :param device: 실행 디바이스 ("cuda" 또는 "cpu")
        :param torch_dtype: torch 데이터 타입 (기본: torch.float16)
        """
        self.base_model_id = base_model_id
        self.lora_path = lora_path
        self.device = device
        self.torch_dtype = torch_dtype
        self._load_pipeline()

    def _load_pipeline(self):
        self.pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
            self.base_model_id,
            torch_dtype=self.torch_dtype
        )
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        if self.lora_path:
            self.pipe.load_lora_weights(self.lora_path)
        self.pipe.to(self.device)

    def generate_images(
        self,
        init_image: Image.Image,
        prompt: str,
        negative_prompt: str,
        strength: float = 1.0,
        guidance_scale: float = 9.5,
        num_images: int = 1,
    ):
        """
        초기 이미지를 기반으로 SDXL Img2Img 변환을 수행하여 이미지를 생성합니다.
        
        :param init_image: 변환할 초기 이미지 (PIL.Image)
        :param prompt: 텍스트 프롬프트
        :param negative_prompt: 네거티브 프롬프트
        :param strength: 원본 이미지 반영 비율 (기본: 1.0)
        :param guidance_scale: 프롬프트 강조 강도 (기본: 9.5)
        :param num_images: 생성할 이미지 수 (기본: 1)
        :return: 생성된 이미지 리스트 (PIL.Image)
        """
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=init_image,
            strength=strength,
            guidance_scale=guidance_scale,
            num_images_per_prompt=num_images,
        )
        return result.images
