from fastapi import Request, HTTPException, APIRouter, Depends, Response # Response 추가 - 김건우
from dotenv import load_dotenv
from typing import Dict
import os
from datetime import datetime, timezone, timedelta
import logging
from ..models.everyQ import book_question
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..database.connections import get_mysql_db
from ..database.crud import read_user, get_user, get_user_by_login
from ..schemas import UserQuestion
from .login import create_access_token # 토큰 생성기 추가 - 김건우

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
async def dupli_check(request: Dict[str, str], mysql_db: Session = Depends(get_mysql_db)):
    """
    id 중복 확인하는 엔드포인트
    """
    try:
        id = request["id"]
        get_user(mysql_db, user_id=id)
        if get_user(mysql_db, user_id=id):
            return { "exists": "true" }
        else: 
            return { "exists": "false"}
        
    except Exception as e:
        raise e
    
# @router.post("/api/local_login")
# async def login_check(request: Dict[str, str],mysql_db: Session = Depends(get_mysql_db)):
#     """
#     로그인하는 엔드포인트
#     """
#     try:
#         user_id = request["id"]
#         user_pw = request["password"]
#         # user_id = id
#         # user_pw = password
    
#         if get_user_by_login(mysql_db, user_id, user_pw):
#             return { "status": "success" }
#         else:
#             return { "status": "failed" }
        
#     except Exception as e:
#         raise e
    

@router.post("/api/local_login")
async def login_check(request: Dict[str, str], response: Response, mysql_db: Session = Depends(get_mysql_db)):
    """
    로그인하는 엔드포인트 (JWT 액세스 토큰을 쿠키에 저장)
    """
    try:
        user_id = request["id"]
        user_pw = request["password"]

        # ✅ 유저 검증 (아이디 & 비밀번호 확인)
        if get_user_by_login(mysql_db, user_id, user_pw):
            # ✅ JWT 액세스 토큰 생성
            access_token = create_access_token(data={"sub": user_id}, expires_in=3600)

            # ✅ 쿠키에 JWT 저장 (HttpOnly & Secure)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,  # JavaScript에서 접근 불가능 (보안 강화)
                secure=True,  # HTTPS에서만 사용 가능 (로컬 개발 시 False로 변경 가능)
                samesite="Lax",  # CSRF 방지
                max_age=3600,  # 60분 유지
            )

            return {"status": "success", "message": "Login successful"}
        else:
            return {"status": "failed", "message": "Invalid username or password"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")