from fastapi import HTTPException, APIRouter, Depends
from dotenv import load_dotenv
import faiss
import numpy as np
import pandas as pd
import http.client
import requests
import json
import time
import re
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database.connections import get_mysql_db, get_postgresql_db
from database.crud import (
    get_users, create_user, get_tokens, create_token, get_books, create_book,
    get_sessions, create_session, get_recommended_books, create_recommended_book,
    get_badges, create_badge, get_reviews, create_review, 
    get_user_questions, create_user_question, get_clova_answers, create_clova_answer
)
from schemas import (
    UserQuestion, ClovaResponse, 
    UserSchema, TokenSchema, BookSchema, SessionSchema, RecommendedBookSchema, 
    BadgeSchema, ReviewSchema, UserQuestionSchema, ClovaAnswerSchema
)

load_dotenv()
CLOVA_Authorization = os.getenv('CLOVA_Authorization')
CLOVA_CHAT_REQUEST_ID = os.getenv('CLOVA_CHAT_REQUEST_ID')
CLOVA_EMBEDDING_REQUEST_ID = os.getenv('CLOVA_EMBEDDING_REQUEST_ID')
router = APIRouter()

def log_message(message, status="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color_code = ""
    if status == "success":
        color_code = "\033[92m"  # 초록색
    elif status == "error":
        color_code = "\033[91m"  # 빨간색
    elif status == "warning":
        color_code = "\033[93m"  # 노란색
    else:
        color_code = "\033[0m"   # 기본색
    
    print(f"{color_code}[{timestamp}] {message}\033[0m")


@router.post("/api/home/ex")
async def book_question(user_question: UserQuestion):
    # 1. 임베딩 전용 클래스
    # class EmbeddingExecutor:
    #     def __init__(self, host, api_key, request_id):
    #         self._host = host
    #         self._api_key = api_key
    #         self._request_id = request_id
    #         self._request_counter = 0

    #     def get_embedding(self, text):
    #         start_time = time.time()
    #         log_message(f"임베딩 생성 시작: '{text[:15]}...'", "info")
    #         headers = {
    #             'Content-Type': 'application/json',
    #             'Authorization': self._api_key,
    #             'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
    #         }

    #         conn = http.client.HTTPSConnection(self._host)
    #         conn.request('POST', 
    #                     '/testapp/v1/api-tools/embedding/v2',
    #                     json.dumps({"text": text}),
    #                     headers)
            
    #         response = conn.getresponse()
    #         result = json.loads(response.read())
    #         conn.close()

    #         # 요청 간 간격 조정 (API 제한 회피)
    #         self._request_counter += 1
    #         if self._request_counter % 10 == 0:
    #             time.sleep(5)
    #         duration = time.time() - start_time
    #         log_message(f"임베딩 생성 완료 ({duration:.2f}s)", "success")
    #         return np.array(result['result']['embedding'], dtype='float32')

    # class ChatCompletionExecutor:
        # def __init__(self, host, api_key, request_id):
        #     self._host = host
        #     self._api_key = api_key
        #     self._request_id = request_id

        # def send_request(self, messages):
        #     start_time = time.time()
        #     log_message("채팅 응답 생성 시작", "info")
        #     headers = {
        #         'Authorization': self._api_key,
        #         'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
        #         'Content-Type': 'application/json'
        #     }

        #     response = requests.post(
        #         f'{self._host}/testapp/v1/chat-completions/HCX-003',
        #         headers=headers,
        #         json={
        #             'messages': messages,
        #             'temperature': 0.9,
        #             'topP': 0.8,
        #             'maxTokens': 4096
        #         },
        #         stream=False
        #     )

        #     for line in response.iter_lines():
        #         if line:
        #             print(line.decode('utf-8'))
        #     log_message("스트리밍 응답 수신 시작", "info")
        #     response_data = []
        #     for line in response.iter_lines():
        #         if line:
        #             response_data.append(line.decode('utf-8'))
            
        #     duration = time.time() - start_time
        #     log_message(f"응답 생성 완료 ({duration:.2f}s)", "success")
        #     return response
    
    class EmbeddingExecutor:
        def __init__(self, host, api_key, request_id):
            self._host = host
            self._api_key = api_key
            self._request_id = request_id
            self._request_counter = 0

        def get_embedding(self, text):
            max_retries = 100
            base_delay = 1  # 초기 지연 시간(초)
            
            for attempt in range(max_retries):
                try:
                    start_time = time.time()
                    log_message(f"임베딩 생성 시도 {attempt+1}/{max_retries}: '{text[:15]}...'", "info")
                    
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': self._api_key,
                        'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
                    }

                    conn = http.client.HTTPSConnection(self._host, timeout=10)
                    conn.request('POST', 
                                '/testapp/v1/api-tools/embedding/v2',
                                json.dumps({"text": text}),
                                headers)
                    
                    response = conn.getresponse()
                    if response.status != 200:
                        raise http.client.HTTPException(f"HTTP 오류: {response.status} {response.reason}")
                    
                    result = json.loads(response.read())
                    conn.close()

                    # 요청 간 간격 조정
                    self._request_counter += 1
                    if self._request_counter % 10 == 0:
                        time.sleep(5)
                        
                    duration = time.time() - start_time
                    log_message(f"임베딩 생성 완료 ({duration:.2f}s)", "success")
                    return np.array(result['result']['embedding'], dtype='float32')

                except (http.client.HTTPException, ConnectionError, TimeoutError) as e:
                    log_message(f"임베딩 요청 실패: {str(e)}", "error")
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay #* (2 ** attempt)  # 지수 백오프
                    time.sleep(delay)

    # 2. 채팅 완료 전용 클래스 
    class ChatCompletionExecutor:
        def __init__(self, host, api_key, request_id):
            self._host = host
            self._api_key = api_key
            self._request_id = request_id

        def send_request(self, messages):
            max_retries = 100
            base_delay = 1  # 초기 지연 시간(초)
            
            for attempt in range(max_retries):
                try:
                    start_time = time.time()
                    log_message(f"채팅 요청 시도 {attempt+1}/{max_retries}", "info")
                    
                    headers = {
                        'Authorization': self._api_key,
                        'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
                        'Content-Type': 'application/json'
                    }

                    response = requests.post(
                        f'{self._host}/testapp/v1/chat-completions/HCX-003',
                        headers=headers,
                        json={
                            'messages': messages,
                            'temperature': 0.9,
                            'topP': 0.8,
                            'maxTokens': 4096
                        },
                        timeout=10,
                        stream=False
                    )
                    response.raise_for_status()  # 4xx/5xx 오류 검출

                    log_message("스트리밍 응답 수신 시작", "info")
                    for line in response.iter_lines():
                        if line:
                            print(line.decode('utf-8'))
                    
                    duration = time.time() - start_time
                    log_message(f"응답 생성 완료 ({duration:.2f}s)", "success")
                    return response

                except (requests.exceptions.RequestException, TimeoutError) as e:
                    log_message(f"채팅 요청 실패: {str(e)}", "error")
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay # * (2 ** attempt) + 0.5  # 지수 백오프 + 지터
                    time.sleep(delay)
    try:
        total_start = time.time()
        log_message("FAISS 인덱스 로드 시작")
        # FAISS 초기화
        index = faiss.read_index("/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/app/apis/vector_store.index")
        data = pd.read_csv("/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/app/apis/final_answers2791까지완료.csv")
        final_answers = data["Final Answer"].tolist()[:2791]
        log_message("FAISS 인덱스 로드 완료", "success")
        ######################################
        # input_text = """빛나 무엇이 빛나나 보자 햇살의 버블팝"""
        ######################################
        log_message("\n" + "="*50)
        log_message("도서 추천 프로세스 시작")
        log_message(f"사용자 입력: {user_question.question}")
        log_message("="*50)

        # 각 단계 시간 측정
        phase_start = time.time()
        log_message("[1/4] 사용자 질문에서 키워드 추출 시작")
        chat_api = ChatCompletionExecutor(
            host='https://clovastudio.stream.ntruss.com',
            api_key=f"Bearer {CLOVA_Authorization}",
            request_id=CLOVA_CHAT_REQUEST_ID
        )

        preset_text = [
            {
                "role": "system",
                "content": f"""**사용자 질문 분석 요청**
    1. 질문: "{user_question.question}" 

    2. 분석 지침:
    - 3계층 키워드 추출 체계 적용
    - 계층별 최소 2개~최대 5개 키워드 생성
    - 동의어 통합 및 불필요한 조사 제거

    3. 계층적 분석 구조:
    [1차] 표면적 키워드:
    - 질문 표면에 명시적으로 나타난 핵심 명사
    - 예시: "요리", "레시피", "식문화"

    [2차] 맥락적 키워드: 
    - 문맥 분석을 통해 도출되는 관련 개념
    - 예시: "식단 계획", "영양 균형", "계절 음식"

    [3차] 잠재적 키워드:
    - 사용자의 숨은 의도 추정을 통한 확장 개념
    - 예시: "식습관 개선", "음식 철학", "지속가능한 식생활"

    4. 출력 형식:
    • 1차: [키워드1, 키워드2, ...] 
    • 2차: [키워드A, 키워드B, ...]
    • 3차: [키워드α, 키워드β, ...]"""
            },{"role":"user","content":"{user_question.question}"}
        ]
        key_word= chat_api.send_request(preset_text)
        key_word=key_word.json()
        key_word_content=key_word['result']['message']['content']
        ######################################
        # 전체 프로세스 단계 표시
        log_message(f"[1/4] 완료 ({time.time()-phase_start:.2f}s)", "success")

        # 각 단계 시간 측정
        phase_start = time.time()
        log_message("[2/4] 임베딩 생성 단계 시작")
        # 1단계: 임베딩 생성
        embedding_api = EmbeddingExecutor(
            host='clovastudio.stream.ntruss.com',
            api_key=f"Bearer {CLOVA_Authorization}",
            request_id=CLOVA_EMBEDDING_REQUEST_ID
        )
        
        query_vector = embedding_api.get_embedding(key_word_content)
        query_vector = query_vector.reshape(1, -1)
        faiss.normalize_L2(query_vector)
        log_message(f"[2/4] 완료 ({time.time()-phase_start:.2f}s)", "success")
        # 2단계: FAISS 검색
        phase_start = time.time()
        log_message("[3/4] 도서 검색 단계 시작")
        distances, indices = index.search(query_vector, 10)
        recommendations = [final_answers[i] for i in indices[0]]
        print(recommendations)
        log_message(f"[3/4] 완료: {len(recommendations)}개 발견 ({time.time()-phase_start:.2f}s)", "success")

        # 3단계: 채팅 응답
        phase_start = time.time()
        log_message("[4/4] 응답 생성 단계 시작")
        # 3단계: 채팅 완료 요청
        chat_api = ChatCompletionExecutor(
            host='https://clovastudio.stream.ntruss.com',
            api_key=f"Bearer {CLOVA_Authorization}",
            request_id=CLOVA_CHAT_REQUEST_ID
        )

        preset_text = [
            {
                "role": "system",
                "content": 
                    f"""- 당신은 지식이 풍부한 도서 큐레이터입니다.
                    - 사용자의 연령과 성별에 맞게 도서를 추천해주세요. 
                    나이 : {user_question.age}세, 성별 : {user_question.gender}
                    - 사용자의 질문과 추천 도서 목록을 기반으로 가장 적합한 책 1권으로 답변합니다.
                    - 답변할 때 recommendation의 우선순위를 생각하지 않고 사용자의 연령과 성별을 반드시 고려해 답변해주세요.
                    - 자연스러운 문장으로 추천 이유를 설명해주세요.
                    - 추천도서 정보만을 사용하여 답변해주세요.
                    - 오타가 발생하지 않게 생성하고 나서 검토를 해주세요.
                    - 답변할 땐 추천할 책 제목만 대답해. 다른 거 말하지 말고 책 제목만!!!
                    답변 예시: 책 제목 : [책 제목]"""
            },
            {
                "role": "user",
                "content": f"질문: {user_question.question}\n추천도서: {', '.join(recommendations)}"
            }
        ]

        response = chat_api.send_request(preset_text)
        log_message(f"[4/4] 완료 ({time.time()-phase_start:.2f}s)", "success")

        # 총 실행 시간
        total_time = time.time() - total_start
        log_message(f"\n전체 프로세스 완료 (총 {total_time:.2f}초 소요)", "success")
        log_message("="*50)
        response_data = []
        for line in response.iter_lines():
            if line:
                response_data.append(line.decode('utf-8'))
        # print(response_data)
        data = json.loads(response_data[0])
        # print(data)
        print(data["result"]["message"]["content"])
        match = re.search(r"책 제목 : (.+)", data["result"]["message"]["content"])

        if match:
            book_title = match.group(1).strip()
        else:
            book_title = None

        # 결과 출력
        print("책 제목:", book_title)
        
        csv_file = pd.read_csv("/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/app/apis/final_answers2791까지완료.csv")

        # 찾고 싶은 책 제목 book_title

        # 해당 책 제목이 있는 행 찾기
        result = csv_file[csv_file["Book Title"] == book_title]

        # 결과 출력
        if not result.empty:
            final_answer = result["Final Answer"].values[0]
            print("Final Answer:", final_answer)
        else:
            print("해당 책 제목을 찾을 수 없습니다.")
        print("================================================")
        print("================================================")

        # 정규식을 사용하여 필요한 정보 추출
        book_title = re.search(r"책 제목 : (.+)", final_answer)
        author = re.search(r"저자 : (.+)", final_answer)
        publisher = re.search(r"출판사 : (.+)", final_answer)
        publish_date = re.search(r"출판일 : (.+)", final_answer)
        isbn = re.search(r"ISBN : (.+)", final_answer)
        description = re.search(r"설명 : (.+?)\n섬네일 링크 :", final_answer, re.DOTALL)
        thumbnail_link = re.search(r"섬네일 링크 : (.+)", final_answer)
        purchase_link = re.search(r"구매링크 : (.+)", final_answer)

        # 추출된 값이 있으면 저장하고, 없으면 빈 문자열로 처리
        book_title = book_title.group(1).strip() if book_title else ""
        author = author.group(1).strip() if author else ""
        publisher = publisher.group(1).strip() if publisher else ""
        publish_date = publish_date.group(1).strip() if publish_date else ""
        isbn = isbn.group(1).strip() if isbn else ""
        description = description.group(1).strip() if description else ""
        thumbnail_link = thumbnail_link.group(1).strip() if thumbnail_link else ""
        purchase_link = purchase_link.group(1).strip() if purchase_link else ""

        # 결과 출력
        print("책 제목:", book_title)
        print("저자:", author)
        print("출판사:", publisher)
        print("출판일:", publish_date)
        print("ISBN:", isbn)
        print("설명:", description)
        print("섬네일 링크:", thumbnail_link)
        print("구매 링크:", purchase_link)

        response_body = ClovaResponse(question=user_question.question,
                                      bookimage=thumbnail_link,
                                      bookTitle=book_title,
                                      description=description)
        return response_body
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Clova API: {e}")
    
# Users API (MySQL)
@router.get("/db/users", response_model=list[UserSchema], tags=["MySQL"])
async def api_get_users(db: Session = Depends(get_mysql_db)):
    """
    Users 테이블 조회
    """
    return get_users(db)

@router.post("/db/users", response_model=UserSchema, tags=["MySQL"])
async def api_create_user(user: UserSchema, db: Session = Depends(get_mysql_db)):
    """
    Users 테이블에 새로운 사용자 추가
    """
    try:
        return create_user(db, user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User 추가 중 오류 발생: {str(e)}")

# Tokens API (MySQL)
@router.get("/db/tokens", response_model=list[TokenSchema], tags=["MySQL"])
async def api_get_tokens(db: Session = Depends(get_mysql_db)):
    """
    Tokens 테이블 조회
    """
    return get_tokens(db)

@router.post("/db/tokens", response_model=TokenSchema, tags=["MySQL"])
async def api_create_token(token: TokenSchema, db: Session = Depends(get_mysql_db)):
    """
    Tokens 테이블에 새로운 토큰 추가
    """
    try:
        return create_token(db, token.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token 추가 중 오류 발생: {str(e)}")

# Books API (MySQL)
@router.get("/db/books", response_model=list[BookSchema], tags=["MySQL"])
async def api_get_books(db: Session = Depends(get_mysql_db)):
    """
    Books 테이블 조회
    """
    return get_books(db)

@router.post("/db/books", response_model=BookSchema, tags=["MySQL"])
async def api_create_book(book: BookSchema, db: Session = Depends(get_mysql_db)):
    """
    Books 테이블에 새로운 책 추가
    """
    try:
         return create_book(db, book.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Book 추가 중 오류 발생: {str(e)}")
    
# Sessions API (MySQL)
@router.get("/db/sessions", response_model=list[SessionSchema], tags=["MySQL"])
async def api_get_sessions(db: Session = Depends(get_mysql_db)):
    """
    Sessions 테이블 조회
    """
    return get_sessions(db)


@router.post("/db/sessions", response_model=SessionSchema, tags=["MySQL"])
async def api_create_session(session: SessionSchema, db: Session = Depends(get_mysql_db)):
    """
    Sessions 테이블에 새로운 세션 추가
    """
    try:
        return create_session(db, session.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session 추가 중 오류 발생: {str(e)}")

# RecommendedBooks API (MySQL)
@router.get("/db/recommended_books", response_model=list[RecommendedBookSchema], tags=["MySQL"])
async def api_get_recommended_books(db: Session = Depends(get_mysql_db)):
    """
    RecommendedBooks 테이블 조회
    """
    return get_recommended_books(db)

@router.post("/db/recommended_books", response_model=RecommendedBookSchema, tags=["MySQL"])
async def api_create_recommended_book(recommended_book: RecommendedBookSchema, db: Session = Depends(get_mysql_db)):
    """
    RecommendedBooks 테이블에 새로운 추천 도서 추가
    """
    try:
        return create_recommended_book(db, recommended_book.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RecommendedBook 추가 중 오류 발생: {str(e)}")

# Badges API (MySQL)
@router.get("/db/badges", response_model=list[BadgeSchema], tags=["MySQL"])
async def api_get_badges(db: Session = Depends(get_mysql_db)):
    """
    Badges 테이블 조회
    """
    return get_badges(db)

@router.post("/db/badges", response_model=BadgeSchema, tags=["MySQL"])
async def api_create_badge(badge: BadgeSchema, db: Session = Depends(get_mysql_db)):
    """
    Badges 테이블에 새로운 배지 추가
    """
    try:
        return create_badge(db, badge.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Badge 추가 중 오류 발생: {str(e)}")

# Reviews API (MySQL)
@router.get("/db/reviews", response_model=list[ReviewSchema], tags=["MySQL"])
async def api_get_reviews(db: Session = Depends(get_mysql_db)):
    """
    Reviews 테이블 조회
    """
    return get_reviews(db)

@router.post("/db/reviews", response_model=ReviewSchema, tags=["MySQL"])
async def api_create_review(review: ReviewSchema, db: Session = Depends(get_mysql_db)):
    """
    Reviews 테이블에 새로운 리뷰 추가
    """
    try:
        return create_review(db, review.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Review 추가 중 오류 발생: {str(e)}")

# UserQuestions API (PostgreSQL)
@router.get("/db/user_questions", response_model=list[UserQuestionSchema], tags=["PostgreSQL"])
async def api_get_user_questions(db: Session = Depends(get_postgresql_db)):
    """
    UserQuestions 테이블 조회  
    """
    return get_user_questions(db)

@router.post("/db/user_questions", response_model=UserQuestionSchema, tags=["PostgreSQL"])
async def api_create_user_question(question: UserQuestionSchema, db: Session = Depends(get_postgresql_db)):
    """
    UserQuestions 테이블에 새로운 질문 추가
    """
    try:
        return create_user_question(db, question.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"UserQuestion 추가 중 오류 발생: {str(e)}")

# ClovaAnswers API (PostgreSQL)
@router.get("/db/clova_answers", response_model=list[ClovaAnswerSchema], tags=["PostgreSQL"])
async def api_get_clova_answers(db: Session = Depends(get_postgresql_db)):
    """
    ClovaAnswers 테이블 조회  
    """
    return get_clova_answers(db)

@router.post("/db/clova_answers", response_model=ClovaAnswerSchema, tags=["PostgreSQL"])
async def api_create_clova_answer(answer: ClovaAnswerSchema, db: Session = Depends(get_postgresql_db)):
    """
    ClovaAnswers 테이블에 새로운 답변 추가  
    """
    try:
        return create_clova_answer(db, answer.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ClovaAnswer 추가 중 오류 발생: {str(e)}")
