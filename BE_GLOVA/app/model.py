import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 위는 얘가 BE_GLOVA를 인식 못해서 쓴 거
from pathlib import Path
# from modelll import get_model

BADGE_DIR = "/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/badge"
Path(BADGE_DIR).mkdir(parents=True, exist_ok=True)

# 임시
def generate_badge(book_title: str, num_images: int = 1) -> list:
    # pipe = get_model()  # 모델 불러오기 현재 모델에 문제가 있어 우선 동작 안하게 주석처리
    prompt = f"octagonal badge with futuristic design, inspired by {book_title}"

    # 이미지 생성
    images = pipe(prompt, num_images_per_prompt=num_images, guidance_scale=7.5).images

    # 이미지 저장
    save_paths = []
    for i, img in enumerate(images):
        filename = f"{book_title.replace(' ', '_')}_{i}.png"
        save_path = Path(BADGE_DIR) / filename
        img.save(save_path)
        save_paths.append(str(save_path))

    return save_paths