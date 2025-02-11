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
    get_user_questions, get_user1_questions, create_user_question, get_clova_answers, create_clova_answer
)
from apis.realhome import (
    api_get_users, api_create_user, api_get_tokens, api_create_token, api_get_books, api_create_book, api_get_sessions, api_create_session, 
    api_get_recommended_books, get_recommended_books_by_user_and_session, api_create_recommended_book, api_get_badges, api_create_badge, api_get_reviews,api_create_review,  api_get_user_questions, api_create_user_question, 
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
from app.apis.home_su import get_user_id
router = APIRouter()
# 이 유저가 추천받은 책들 겟 
@router.get("/api/get_books")
async def get_books(
    postgresql_db: Session = Depends(get_postgresql_db),
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)
):
    try:
        question_recommendedBook = []
        # 유저 id인 유저 퀘스션을 모두 찾아.
        user_questions = get_user1_questions(postgresql_db, user_id)

        # 세션 id를 하나하나 돌면서 유저 퀘스션 그 값과 레커멘디드 북스 (유저id세션id) 그 값을 묶어
        for question in user_questions:
            recommended_book = get_recommended_books_by_user_and_session(mysql_db, user_id, question.session_id)
            question_recommendedBook.append([question, recommended_book])
        
        # 리스트에 유저퀘스션-레커멘디드북 쌍으로 모두 리턴
        return {
            "status": "success",
            "message": " successfully",
            "response_body": question_recommendedBook
        }
        
    except Exception as e:
        raise e

# 책 하나를 눌름     
@router.get("/api/get_book")
async def get_book(
    book_id: str,
    mysql_db: Session = Depends(get_mysql_db),
):
    try:
        return get_book(mysql_db, book_id)
    
    except Exception as e:
        raise e



