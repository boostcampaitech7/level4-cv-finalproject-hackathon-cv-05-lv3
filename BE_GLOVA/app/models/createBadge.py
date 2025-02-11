import os
# 추론코드 그대로
# 책 표지, 프롬프트 넣을 것만 생각
from models.badge_creator.main import main

def generate_badge(book_img: str):
    try:
        # ✅ 현재 스크립트(`createBadge.py`)가 위치한 디렉토리를 기준으로 상대 경로 설정
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로 가져오기
        OUTPUT_DIR = os.path.join(BASE_DIR, "badge_creator", "badge_img")  # 상대 경로 지정
        LORA_PATH = os.path.join(BASE_DIR, "badge_creator", "badgemkrsdxl.safetensors")

        print(f"✅ Output directory: {OUTPUT_DIR}")
        print(f"✅ LoRA model path: {LORA_PATH}")   

        # ✅ 디렉토리 생성 (존재하지 않으면)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        png = main(OUTPUT_DIR, book_img, LORA_PATH)
        
        return png
    
    except Exception as e:
        raise e
    
    finally:
        if os.path.exists(OUTPUT_DIR):
            for file in os.scandir(OUTPUT_DIR):
                print("Remove File: ",file)
                os.remove(file)
