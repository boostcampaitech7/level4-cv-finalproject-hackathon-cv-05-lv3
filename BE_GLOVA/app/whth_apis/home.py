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
    UserQuestion, ClovaResponse, 
    UserSchema, TokenSchema, BookSchema, SessionSchema, RecommendedBookSchema, 
    BadgeSchema, ReviewSchema, UserQuestionSchema, ClovaAnswerSchema
)
import logging
from models.everyQ import book_question

load_dotenv()

router = APIRouter()

def get_user_data(user_id: str, db: Session = Depends(get_mysql_db)):
    user = read_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def current_age(birth_year: str) -> int:
    try:
        KST = timezone(timedelta(hours=9))
        current_year = datetime.now(KST).year
        return current_year - int(birth_year) # 한국 나이란 뭘까... 
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid birth year format")

# 사용자가 무물을 한 번 써봤을 때
@router.post("/home")
async def every_Q(question: str, user_id: str, db: Session = Depends(get_mysql_db)):
    try:
        # 사용자 나이, 성별 불러오기 user.gender user.birth_year
        # 어디 토큰에서 뭐 유저 id 가져올 수 있는 거 같음...?
        user = get_user_data(user_id, db)
        age = current_age(user.birth_year)
        
        # 각 데이터를 에브리 큐 함수에 넣기
        response = book_question(question=question, age=age, gender=user.gender)
        # 답변 리턴
        return response
    
    except Exception as e:
        raise e
    except Exception as e:
        # 알 수 없는 예외 처리
        logging.error(f"서버 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 사용자가 이 답변을 저장하고자 할 때
@router.post("/api/save_books", tags=["PostgreSQL"])
async def save_books(question_text: str, db: Session = Depends(get_postgresql_db)):
    try:
        # 유저 퀘스션 포스트 
        question_data = UserQuestionSchema(user_id=user_id, session_id=?, question_text=question_text)
        response1 = await api_create_user_question(question_data, db)
        
        # 클로바 엔써 포스트
        answer = ClovaAnswerSchema(answer_text={book_title, book_description})
        response2 = await api_create_clova_answer(answer=answer, db)
        
        # 북스 포스트트
        book = BookSchema() # 이건 프론트에게 통째로 받으면 될수도?
        response3 = await api_create_book(book, db)
        
        # 4. 레커멘테이션 북스 포스트
        recommended_book= RecommendedBookSchema # 수현쓰한테 질문 : 이건 다 알아서 생성되는 느낌 같은데 유저 id만 넣으면 되는 건가...??
        response4 = await api_create_recommended_book(recommended_book, db)

        return {
            "status": "success",
            "responses": [response1, response2, response3, response4]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch Process 중 오류 발생: {str(e)}")

