import os
import cv2
from PIL import Image
from badge_color import extract_dominant_colors, create_central_circle_image
from badge_generator import SDXLBadgeGenerator
from badge_remover import remove_background_from_image

def main(output_dir, img, lora_path):
    # 1. 파일 경로 설정
    # input_image_path = "/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/app/models/badge_creator/image.png"  # 색상 추출용 원본 이미지 경로 (환경에 맞게 수정)
    # output_dir = "/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/app/models/badge_creator/badge_img"
    # os.makedirs(output_dir, exist_ok=True)
    
    # 2. dominant 색상 추출 및 뱃지 배경 생성
    # img = cv2.imread(input_image_path)
    # if img is None:
    #     print("입력 이미지를 불러올 수 없습니다:", input_image_path)
    #     return
    dominant_colors = extract_dominant_colors(img, k=3)
    badge_bg = create_central_circle_image(dominant_colors, canvas_size=1024, circle_diameter=512)
    # badge_bg_path = os.path.join(output_dir, "badge_background.jpg")
    # cv2.imwrite(badge_bg_path, badge_bg)
    # print("배경 이미지 저장:", badge_bg_path)
    
    # 3. OpenCV(BGR) 이미지를 PIL(RGB) 이미지로 변환 및 리사이즈
    badge_bg_rgb = cv2.cvtColor(badge_bg, cv2.COLOR_BGR2RGB)
    init_image = Image.fromarray(badge_bg_rgb).resize((1024, 1024))
    
    # 4. SDXL Img2Img를 이용한 뱃지 이미지 생성
    prompt = "hexagon with a majestic Cow wearing a crown, vector, logo, badge, best quality"
    negative_prompt = "bad art, low quality, deformed, blurry, watermark, text, realistic photo"
    # lora_path = "/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/app/models/badge_creator/badgemkrsdxl.safetensors"  # 환경에 맞게 수정
    badge_generator = SDXLBadgeGenerator(lora_path=lora_path)
    generated_images = badge_generator.generate_images(
        init_image=init_image,
        prompt=prompt,
        negative_prompt=negative_prompt,
        strength=1.0,
        guidance_scale=9.5,
        num_images=1
    )
    for i, img in enumerate(generated_images):
        img_path = os.path.join(output_dir, f"sdxl_badge_result_{i}.png")
        img.save(img_path)
        print("생성된 뱃지 이미지 저장:", img_path)
    
    # 5. 배경 제거: 첫 번째 생성 이미지에 대해 배경 제거 실행
    input_removal_path = os.path.join(output_dir, "sdxl_badge_result_0.png")
    output_removal_path = os.path.join(output_dir, "sdxl_badge_result_0_no_bg.png")
    png_data = remove_background_from_image(input_removal_path, output_removal_path)
    print("배경 제거된 이미지 저장:", output_removal_path)
    return png_data

# if __name__ == '__main__':
#     main()
