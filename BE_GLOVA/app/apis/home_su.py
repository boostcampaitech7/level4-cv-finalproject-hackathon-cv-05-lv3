from fastapi import Request, HTTPException, APIRouter, Depends
from dotenv import load_dotenv
import faiss
import numpy as np
import pandas as pd
import http.client
import requests
import json
import time
import re
from typing import Dict
from pydantic import BaseModel
import os
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from database.connections import get_mysql_db, get_postgresql_db
from database.crud import (
    get_users, create_user, read_user, get_tokens, create_token, get_books, create_book,
    get_sessions, create_session, get_recommended_books, create_recommended_book,
    get_badges, create_badge, get_reviews, create_review, 
    get_user_questions, create_user_question, get_clova_answers, create_clova_answer
)
from apis.realhome import (
    api_get_users, api_create_user, api_get_tokens, api_create_token, api_get_books, api_create_book, api_get_sessions, api_create_session, 
    api_get_recommended_books, api_create_recommended_book, api_get_badges, api_create_badge, api_get_reviews,api_create_review,  api_get_user_questions, api_create_user_question, 
    api_get_clova_answers, api_create_clova_answer 
)
from schemas import (
    UserQuestion, ClovaResponse, CalendarResponse,
    UserSchema, TokenSchema, BookSchema, SessionSchema, RecommendedBookSchema, 
    BadgeSchema, ReviewSchema, UserQuestionSchema, ClovaAnswerSchema
)
import logging
from models.everyQ import book_question
from jose import JWTError, jwt
import secrets

# 환경 변수에서 Secret Key 가져오기
NAVER_LOGIN_CLIENT_SECRET = os.getenv('NAVER_LOGIN_CLIENT_SECRET')
ALGORITHM = "HS256"

load_dotenv()

router = APIRouter()

def get_user_id(request: Request, db: Session = Depends(get_mysql_db)) -> str:
    """
    - 쿠키에서 JWT access_token을 가져와 디코딩하여 user_id를 추출
    - 추출한 user_id가 DB에 존재하는지 검증 후 반환
    """
    # ✅ 1. 쿠키에서 access_token 가져오기
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")  # ❌ 토큰 없음

    try:
        # ✅ 2. JWT 토큰 디코딩하여 user_id 추출
        payload = jwt.decode(access_token, NAVER_LOGIN_CLIENT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")  # ❌ 토큰에서 user_id 없음

        # ✅ 3. DB에서 user_id 확인
        user = read_user(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User does not exist")  # ❌ 유저 없음

        return user_id  # ✅ 유효한 user_id 반환

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")  # ❌ JWT 인증 실패

def current_age(birth_year: str) -> int:
    try:
        KST = timezone(timedelta(hours=9))
        current_year = datetime.now(KST).year
        return current_year - int(birth_year)  # 한국 나이란 뭘까... 
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid birth year format")

@router.post("/api/home")
async def every_Q(
    request: ClovaAnswerSchema,  # ✅ 클라이언트에서 `body`로 전달된 데이터 받기
    db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)  # ✅ JWT 토큰에서 `user_id` 가져오기
) -> Dict:
    """
    유저 나이, 성별을 기반으로 책 추천 질문을 처리하는 엔드포인트
    """
    try:
        # 질문을 기반으로 도서 추천 처리
        response = book_question(
            question=request.question,
            age=request.age,
            gender=request.gender
        )
        if not response:
            raise HTTPException(status_code=500, detail="추천 결과를 가져올 수 없습니다.")

        return {"status": "success", "data": response}  # ✅ JSON 형식으로 응답
    except Exception as e:
        logging.error(f"서버 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
def generate_session_id():
    """ 랜덤한 세션 ID 생성 (32자리) """
    return secrets.token_hex(16)

def parse_datetime(date_str: str, time_str: str) -> datetime:
    """ ✅ 클라이언트에서 받은 날짜와 시간을 조합하여 datetime 객체로 변환 """
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

# 사용자가 이 답변을 저장하고자 할 때
@router.post("/api/save_books")
async def save_books(
    request: Dict[str, str],  # ✅ 클라이언트에서 JSON 데이터를 받음
    postgresql_db: Session = Depends(get_postgresql_db),
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)
):
    try:
        # ✅ 1️⃣ 클라이언트에서 받은 date & time을 이용해 timestamp 생성
        timestamp = parse_datetime(request["date"], request["time"])

        # ✅ 2. 새로운 세션 ID 생성
        session_id = generate_session_id()

        # ✅ 3️⃣ 질문 테이블에 데이터 저장 (PostgreSQL)
        question_data = UserQuestionSchema(
            user_id=user_id,
            session_id=session_id,
            question_text={"질문": request["question"]},
            created_at=timestamp
        )
        question_response = await create_user_question(question_data, db=postgresql_db)

        # book_id, book_title은 미리 저장된 books 테이블에서 조회

        # ✅ 4️⃣ 클로바 답변 테이블에 데이터 저장 (PostgreSQL)
        answer_data = ClovaAnswerSchema(
            user_id=user_id,
            session_id=session_id,
            answer_text={"책 제목": book_title, "추천 이유": request["description"]},
            created_at=timestamp
        )
        answer_response = await create_clova_answer(answer_data, db=postgresql_db)


        # ✅ 6️⃣ 추천 도서 테이블에 데이터 저장 (MySQL)
        recommended_book_data = RecommendedBookSchema(
            user_id=user_id,
            book_id=book_id,
            session_id=session_id,
            recommended_at=timestamp,
            finished_at=None
        )
        recommended_book_response = await create_recommended_book(recommended_book_data, db=mysql_db)

        # ✅ 7️⃣ 세션 테이블에 데이터 저장 (MySQL)
        session_data = SessionSchema(
            session_id=session_id,
            question_id=question_response.question_id,
            answer_id=answer_response.answer_id
        )
        session_response = await create_session(session_data, db=mysql_db)

        return {
            "status": "success",
            "message": "Book data saved successfully",
            "session_id": session_id,
            "stored_data": {
                "question": question_response,
                "answer": answer_response,
                "book": book_title,
                "recommended_book": recommended_book_response,
                "session": session_response
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch Process 중 오류 발생: {str(e)}")
