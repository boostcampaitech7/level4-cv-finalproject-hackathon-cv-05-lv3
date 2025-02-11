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
from ..database.connections import get_mysql_db, get_postgresql_db
from ..database.crud import (
    get_users, create_user, read_user, get_tokens, create_token, get_books, get_book, create_book,
    get_sessions, create_session, get_recommended_books, create_recommended_book,
    get_badges, get_user_badge, create_badge, get_reviews, get_book_reviews, create_review, 
    get_user_questions, get_user1_questions, create_user_question, get_clova_answers, create_clova_answer
)
from apis.realhome import (
    api_get_users, api_create_user, api_get_tokens, api_create_token, api_get_books, api_create_book, api_get_sessions, api_create_session, 
    api_get_recommended_books, get_recommended_books_by_user_and_session, api_create_recommended_book, api_get_badges, api_create_badge, api_get_reviews,api_create_review,  api_get_user_questions, api_create_user_question, 
    api_get_clova_answers, api_create_clova_answer 
)
from ..schemas import (
    UserQuestion, ClovaResponse, CalendarResponse,
    UserSchema, TokenSchema, BookSchema, SessionSchema, RecommendedBookSchema, 
    BadgeSchema, ReviewSchema, UserQuestionSchema, ClovaAnswerSchema
)
import logging
from models.everyQ import book_question
from jose import JWTError, jwt
import secrets
from app.apis.home_su import get_user_id, parse_datetime

from app.models.createBadge import create_badge
# from app.models.createVoice import clova_voice
router = APIRouter()

# 이 책에 대한 리뷰 작성 페이지로 감. 많은 후기들이 있으면 보여짐
# 프론트가 유저 id인 리뷰 찾고싶음 찾으라고 user_id도 줬음
# 이 리뷰 쓴 사람이 이 책을 읽고 뱃지 만들엇으면 뱃지도 넣어야함 
@router.get("/api/get_book_reviews")
async def get_book_reviews_badges(
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id),
    book_id: str
):
    try:
        reviews = get_book_reviews(db=mysql_db, book_id)
        
        review_badge = []
        for review in reviews:
            if get_user_badge(mysql_db, user_id=review.user_id, book_id):
                review_badge.append([review, get_user_badge(mysql_db, user_id=review.user_id, book_id)])
            else:
                review_badge.append([review, -1]) # 프론트야 -1이 뜨면 뱃지 없는 사람이라고 생각해줘.
            
        return  {
            "review_badge": review_badge,
            "user_id": user_id # 이걸로 내가 리뷰 썼으면 맨 위에 올려줘
        }
    
    except Exception as e:
        raise e

# 리뷰 작성은 잇고 ㅇㅇ

