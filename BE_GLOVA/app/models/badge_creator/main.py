import os
import cv2
import random
import string
from PIL import Image
from .badge_color import extract_dominant_colors, create_central_circle_image
from .badge_generator import SDXLBadgeGenerator
from .badge_remover import remove_background_from_image

def main(output_dir, img, lora_path):
    # 2. dominant 색상 추출 및 뱃지 배경 생성
    dominant_colors = extract_dominant_colors(img, k=3)
    badge_bg = create_central_circle_image(dominant_colors, canvas_size=1024, circle_diameter=512)
    
    # 3. OpenCV(BGR) 이미지를 PIL(RGB) 이미지로 변환 및 리사이즈
    badge_bg_rgb = cv2.cvtColor(badge_bg, cv2.COLOR_BGR2RGB)
    init_image = Image.fromarray(badge_bg_rgb).resize((1024, 1024))
    
    # 4. 프롬프트 설정: 0.03% 확률로 고정 프롬프트 사용, 아니면 12지신 중 랜덤 선택
    if random.random() < 0.0003:  # 0.03% 확률
        prompt = "a hexagon with a fairy , vector, best quality, badgemkrsdxl, white background,fantasy, beautiful, cute, magical, badg"
    else:
        zodiac_animals = [
            "Rat", "Cow", "Tiger", "Rabbit", "Dragon", "Snake",
            "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
        ]
        chosen_animal = random.choice(zodiac_animals)
        prompt = f"hexagon with a majestic {chosen_animal} wearing a crown, vector, logo, badge, best quality"
    
    negative_prompt = "bad art, low quality, deformed, blurry, watermark, text, realistic photo"
    
    # 5. SDXL Img2Img를 이용한 뱃지 이미지 생성 (1장만 생성)
    badge_generator = SDXLBadgeGenerator(lora_path=lora_path)
    generated_image = badge_generator.generate_images(
        init_image=init_image,
        prompt=prompt,
        negative_prompt=negative_prompt,
        strength=1.0,
        guidance_scale=9.5,
        num_images=1
    )[0]
    
    # 6. 파일명 20자리 랜덤 문자열 생성 후 이미지 저장
    base_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    img_path = os.path.join(output_dir, f"{base_filename}.png")
    generated_image.save(img_path)
    print("생성된 뱃지 이미지 저장:", img_path)
    
    # 7. 배경 제거: 저장한 이미지에 대해 배경 제거 실행 (출력 파일명도 20자리 랜덤 문자열)
    removal_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    input_removal_path = img_path
    output_removal_path = os.path.join(output_dir, f"{removal_filename}.png")
    png_data = remove_background_from_image(input_removal_path, output_removal_path)
    print("배경 제거된 이미지 저장:", output_removal_path)
    
    return output_removal_path