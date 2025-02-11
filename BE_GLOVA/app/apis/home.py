from fastapi import Request, HTTPException, APIRouter, Depends
from dotenv import load_dotenv
from typing import Dict
import os
from datetime import datetime, timezone, timedelta
import logging
from models.everyQ import book_question
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database.connections import get_mysql_db
from database.crud import read_user, get_user
from schemas import UserQuestion

router = APIRouter()

def current_age(birth_year: str) -> int:
    try:
        KST = timezone(timedelta(hours=9))
        current_year = datetime.now(KST).year
        return current_year - int(birth_year)  # 한국 나이란 뭘까... 
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid birth year format")

@router.post("/api/home")
async def every_Q(
    request: UserQuestion,  # ✅ 클라이언트에서 `body`로 전달된 데이터 받기
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


@router.post("/api/dupli_check")
async def dupli_check(id: str, mysql_db: Session = Depends(get_mysql_db)):
    """
    id 중복 확인하는 엔드포인트
    """
    try:
        # 질문을 기반으로 도서 추천 처리
        get_user(mysql_db, user_id=id)
        if get_user(mysql_db, user_id=id):
            return { "exists": "true" }
        else:
            return { "exists": "false"}
        
    except Exception as e:
        raise e