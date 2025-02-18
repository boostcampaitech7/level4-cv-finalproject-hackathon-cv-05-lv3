# HiBookGlova (하이북글로바)

<p align="center">
  <img width="400" alt="main_image" src="https://github.com/user-attachments/assets/3c0a22d3-c15e-4856-aaf4-8093010fb2d0" />
</p>

## 프로젝트 소개
"하이북글로바"는 가볍고 재미있게 독서를 즐길 수 있도록 돕는 서비스입니다. SNS 감성의 [무엇이든 물어보세요]기능, 위시 리스트 피드, 독서 뱃지 생성 등을 통해 MZ 세대의 독서 경험을 더욱 특별하게 만듭니다.📚✨

<br/>

### 하이북클로바 실행 방법
```
git clone https://github.com/boostcampaitech7/level4-cv-finalproject-hackathon-cv-05-lv3.git

docker-compose up --build -d
```

## ✨ Key Features & Achievements
1. **무물(무엇이든 물어보세요) 형식**  
   - 인스타그램 “무물” 형식을 차용  
   - 유저가 부담 없이 질문하면, AI가 상황을 파악하여 적합한 **도서를 추천**  
   - 예: “면접을 앞두고 너무 긴장돼요. 마음을 편하게 해줄만한 책 없을까요?”

2. **RAG 기반 도서 임베딩 DB**  
   - 약 **115,419권의 도서**를 벡터화하여 FAISS에 저장  
   - 존재하지 않는 도서를 잘못 추천(할루시네이션)하는 문제를 해결해, **정확도 0.99** 달성

3. **최신 도서 자동 갱신**  
   - **Airflow 파이프라인**을 적용하여 매주 새로운 도서 데이터를 반영  
   - **데이터 최신화** 유지로, 계속해서 신선한 책 추천

4. **다차원적 질문 분석: Multi-Query Retriever**  
   - 질문을 **Explicit/Contextual/Latent** 3가지로 쪼개어 처리 후 통합  
   - 사용자 질문의 맥락과 잠재 의도를 고려해 **공감력 높은 추천** 구현  
   - 사용자 **답변 만족도 0.86** 달성

5. **SNS형 위시 리스트 & 독서 뱃지**  
   - SNS 피드처럼 위시 리스트 관리  
   - **책 표지**를 활용해 완독 시 **맞춤형 뱃지**를 자동 생성

<br/>


<br/>

## 주요 기능 사용방식
### 📖 무엇이든 책으로 대답합니다!
궁금한 점이 있다면 "무엇이든 물어보세요" 기능을 사용해 보세요.  
AI가 질문을 분석하고, 관련된 책을 찾아 추천해 줍니다.

### 📚 도서 위시 리스트를 깔끔한 피드로!
읽고 싶은 책을 저장하고, 위시 리스트를 SNS 피드 형태로 관리하세요.
깔끔하게 정리된 책 목록을 한눈에 확인할 수 있습니다.  

### 🏅 다 읽었어요~! 뱃지를 생성합니다
책을 다 읽으면 책 표지를 바탕으로 단 하나뿐인 뱃지를 생성합니다.
나만의 독서 기록을 남기고, 뱃지를 모아보는 재미를 느껴보세요!  

### 👥 이 책 어때요? 이런 점이 좋았어요!
책에 대한 감상평, 기대, 그밖에 다양한 코멘트를 작성할 수 있습니다.
이를 다양한 사람들과 함께 공유해보세요.
<br/>
| ![image (1)](https://github.com/user-attachments/assets/3481bf92-def9-4761-b686-3ba3d7c04a24) | ![image (2)](https://github.com/user-attachments/assets/a2f4dce8-0683-4e1c-a6fe-a522aaf152f1) | ![image (3)](https://github.com/user-attachments/assets/717b7da9-5c29-4822-9da7-1765aacd7084) |
|---|---|---|

| ![image (4)](https://github.com/user-attachments/assets/154544c9-ccc2-4481-a414-613c5d0638b9) | ![image (5)](https://github.com/user-attachments/assets/69f448f0-e168-492e-862c-e4831de1c838) | ![image (6)](https://github.com/user-attachments/assets/4ae297b3-e369-496d-b3b0-0bc8cf16f047) | 
|---|---|---|
<br/>


> ## 👥 팀 소개
| 김건우 | 김범조 | 김석현 | 임홍철 | 정수현 | 조소윤 |
|:------:|:------:|:------:|:------:|:------:|:------:|
| <img src="https://avatars.githubusercontent.com/u/74577797?v=4" alt="김건우" width="150"> | <img src="https://avatars.githubusercontent.com/u/61742009?v=4" alt="김범조" width="150"> | <img src="https://avatars.githubusercontent.com/u/80832362?v=4" alt="김석현" width="150"> | <img src="https://avatars.githubusercontent.com/u/49517864?v=4" alt="임홍철" width="150"> | <img src="https://avatars.githubusercontent.com/u/90364745?v=4" alt="정수현" width="150"> | <img src="https://github.com/user-attachments/assets/22baca4a-189a-4bc3-ab1c-8f6256637a16" alt="조소윤" width="150"> |
| [GitHub](https://github.com/KOKOLOCOKES) | [GitHub](https://github.com/8eomio) | [GitHub](https://github.com/kimsuckhyun) | [GitHub](https://github.com/limhongcheol) | [GitHub](https://github.com/suhyun6363) | [GitHub](https://github.com/whthdbs03) | 
<br/>
<br/>


## 🔧 Tech Stack

| Category                  | Tech                                     |
|---------------------------|------------------------------------------|
| **Backend**               | FastAPI, Python, Airflow                 |
| **Frontend**              | React.js, Node.js                        |
| **Database**              | MySQL, PostgreSQL                        |
| **Vector Search & IR**    | FAISS, BGE-M3, NAVER OpenAPI             |
| **LLM & AI**              | HyperCLOVA X, PyTorch, Diffusers         |
| **Infra & Deployment**    | Docker, Docker Compose                   |
| **Collaboration & DevOps**| Git/GitHub, Notion, Slack                |

## 🏛️ 전체 서비스 아키텍처
#### 1. 서비스 요청 흐름도
<img width="794" alt="image (9)" src="https://github.com/user-attachments/assets/0e999a6f-4c48-4590-b276-9c1390b1e5e2" />  

#### 2. 모델 아키텍처
<img width="941" alt="image (1)" src="https://github.com/user-attachments/assets/7a7909c6-3356-456e-baaa-bbbcbaaf743b" />  
<br/>

## 🗓️ 프로젝트 타임라인
<img width="885" alt="image (7)" src="https://github.com/user-attachments/assets/ee2965fa-c9ed-47ae-95f0-ab13e71eee39" />
<br/>

## ⚙️ Additional Resources
- [📚 발표 자료 PDF](https://github.com/user-attachments/files/18751070/CV_5._._.pdf)  
- [🍀 Notion 페이지](https://slash-english-359.notion.site/HiBookGLOVA-4665f5a0215f4f44bd140bbb2a35026c?pvs=74)

   
