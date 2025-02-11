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
    get_badges, create_badge, get_reviews, create_review, 
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

# 보이스 x 걍 뱃지만! 
@router.post("/api/badge")
async def create_badge(
    request: Dict[str, str, str],  # date, time, book_id
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)  # ✅ JWT 토큰에서 `user_id` 가져오기
) -> Dict:
    """
    뱃지랑 보이스를 만들어서 리턴!
    책 표지로 뱃지 이미지 만들어서 받고
    이미지랑 url이랑 시간 만들고, 북id랑 유저 id넣어서 뱃지 테이블 생성
    북 이미지랑 mp3 리턴? 그냥 테이블 쨰로 리턴 
    """
    try:
        # ✅ 1️⃣ 클라이언트에서 받은 date & time을 이용해 timestamp 생성
        timestamp = parse_datetime(request["date"], request["time"])
        
        book_detail = get_book(mysql_db, request["book_id"])
        
        png_data = create_badge(book_detail.image)
        
        badge = BadgeSchema(
            user_id=user_id,
            book_id=request["book_id"],
            badge_image=png_data, #?
            created_at=timestamp
        )
        badge_response = await api_create_badge(badge, mysql_db)
        
        return {
            "status": "success",
            "message": "Badge saved successfully",
            "stored_data": badge_response
        }

    except Exception as e:
        raise e
        
     
@router.get("/api/userBadges", response_model=list[BadgeSchema], tags=["MySQL"])
async def get_user_badges(
    db: Session = Depends(get_mysql_db), 
    user_id: str = Depends(get_user_id)
):
    '''
    한 유저가 갖고있는 뱃지들 조회
    '''
    return get_user_badges(db, user_id)      

  