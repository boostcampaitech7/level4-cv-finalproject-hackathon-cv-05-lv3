import os
# 추론코드 그대로
# 책 표지, 프롬프트 넣을 것만 생각
from badge_creator.main import main

def create_badge(book_img: str):
    try:
    # 파일 경로 설정
        output_dir = "/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/app/models/badge_creator/badge_img"
        os.makedirs(output_dir, exist_ok=True)
        
        lora_path = "/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/app/models/badge_creator/badgemkrsdxl.safetensors"
        
        png = main(output_dir, book_img, lora_path)
        
        return png
    
    except Exception as e:
        raise e
    
    finally:
        if os.path.exists(output_dir):
            for file in os.scandir(output_dir):
                print("Remove File: ",file)
                os.remove(file)
