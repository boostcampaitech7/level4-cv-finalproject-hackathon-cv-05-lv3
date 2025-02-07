# badge_creator/main.py
import os
import cv2
from PIL import Image
from badge_creator.badge_color import extract_dominant_colors, create_central_circle_image
from badge_creator.badge_generator import SDXLBadgeGenerator

def main():
    # 사용자 설정
    input_image_path = "/home/sh/nvidia/data/test01.jpg"  # 색상 추출용 원본 이미지 경로
    output_dir = "/home/sh/nvidia/data/generated_badges"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 색상 추출 및 배경 생성
    img = cv2.imread(input_image_path)
    if img is None:
        print("입력 이미지를 불러올 수 없습니다. 경로를 확인하세요.")
        return

    dominant_colors = extract_dominant_colors(img, k=3)
    badge_bg = create_central_circle_image(dominant_colors, canvas_size=1024, circle_diameter=512)
    
    badge_bg_path = os.path.join(output_dir, "badge_background.jpg")
    cv2.imwrite(badge_bg_path, badge_bg)
    print(f"배지 배경 이미지가 '{badge_bg_path}' 에 저장되었습니다.")

    # OpenCV(BGR)를 PIL(RGB)로 변환 및 리사이즈
    badge_bg_rgb = cv2.cvtColor(badge_bg, cv2.COLOR_BGR2RGB)
    init_image = Image.fromarray(badge_bg_rgb).resize((1024, 1024))
    
    # 2. SDXL Img2Img를 이용하여 배지 이미지 생성
    prompt = "hexagon, vector, faith, trust, white background, best quality,"
    negative_prompt = "bad art, low quality, deformed, blurry, watermark, text, realistic photo"
    
    lora_path = "/home/sh/nvidia/data/badgemkrsdxl.safetensors"  # 환경에 맞게 수정
    badge_generator = SDXLBadgeGenerator(lora_path=lora_path)
    
    generated_images = badge_generator.generate_images(
        init_image=init_image,
        prompt=prompt,
        negative_prompt=negative_prompt,
        strength=1.0,
        guidance_scale=9.5,
        num_images=4
    )
    
    for i, img in enumerate(generated_images):
        img_path = os.path.join(output_dir, f"sdxl_badge_result_{i}.png")
        img.save(img_path)
        print(f"생성된 배지 이미지가 '{img_path}' 에 저장되었습니다.")

if __name__ == '__main__':
    main()
