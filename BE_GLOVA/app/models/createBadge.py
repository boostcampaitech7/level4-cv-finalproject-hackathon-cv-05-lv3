import os
# 추론코드 그대로
# 책 표지, 프롬프트 넣을 것만 생각
from models.badge_creator.main import main

def generate_badge(book_img: str):
    try:
        # ✅ 현재 스크립트(`createBadge.py`)가 위치한 디렉토리를 기준으로 상대 경로 설정
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        # ✅ 기존 LoRA 모델 경로 유지 (app/models/badge_creator/)
        LORA_DIR = os.path.join(BASE_DIR, "app", "models", "badge_creator")
        LORA_PATH = os.path.join(LORA_DIR, "badgemkrsdxl.safetensors")

        # ✅ 'data/' 폴더 설정 (뱃지 이미지는 여기에 저장)
        DATA_DIR = os.path.join(BASE_DIR, "data")
        os.makedirs(DATA_DIR, exist_ok=True)  # ✅ 'data' 폴더가 없으면 생성

        # ✅ 이미지 저장 경로 설정
        OUTPUT_DIR = os.path.join(DATA_DIR, "badge_img")
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # ✅ 디렉토리 생성
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        print(f"✅ Output directory: {OUTPUT_DIR}")
        print(f"✅ LoRA model path: {LORA_PATH}")   
        
        png = main(OUTPUT_DIR, book_img, LORA_PATH)
        
        return png
    
    except Exception as e:
        raise e
    
