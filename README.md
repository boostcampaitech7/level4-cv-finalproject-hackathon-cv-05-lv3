# Badge Creator

이 프로젝트는 배지 생성과 관련된 기능을 모듈화한 예제입니다.  
두 가지 주요 기능을 포함합니다:

1. **배지 색상 추출 및 배경 생성**  
   - 입력 이미지에서 dominant 색상 3개를 추출한 후, 중앙 원 형태의 배경(배지)을 생성합니다.

2. **SDXL Img2Img를 이용한 배지 이미지 생성**  
   - 생성된 배경 이미지를 초기 이미지로 사용하여 SDXL Img2Img 파이프라인을 통해 최종 배지 이미지를 생성합니다.

## 파일 구조

```
level4-cv-finalproject-hackathon-cv-05-lv3/
├── badge_creator/
│   ├── __init__.py
│   ├── badge_color.py
│   ├── badge_generator.py
│   └── main.py
├── README.md
└── requirements.txt
```

## 설치 및 실행

1. feat-9/lora-img2img-dataset 브랜치만 클론:

   ```bash
   git clone -b feat-9/lora-img2img-dataset --single-branch git@github.com:boostcampaitech7/level4-cv-finalproject-hackathon-cv-05-lv3.git
   cd level4-cv-finalproject-hackathon-cv-05-lv3
   ```

2. 필요한 라이브러리 설치:

   ```bash
   pip install torch diffusers transformers peft safetensors opencv-python pillow
   ```

3. 예제 실행:

   ```bash
   python badge_creator/main.py
   ```

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.