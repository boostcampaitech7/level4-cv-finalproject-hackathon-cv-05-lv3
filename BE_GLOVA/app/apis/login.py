from fastapi import FastAPI, Request, Depends, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
import requests
from pydantic import BaseModel
import httpx
import os
import urllib.parse
from dotenv import load_dotenv
import secrets
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database.crud import (
    read_user, create_user, read_token, create_token
)
from database.connections import get_mysql_db

router = APIRouter()

# 환경 변수 로드
load_dotenv()

# 환경 변수
NAVER_LOGIN_CLIENT_ID = os.getenv('NAVER_LOGIN_CLIENT_ID')
NAVER_LOGIN_CLIENT_SECRET = os.getenv('NAVER_LOGIN_CLIENT_SECRET')
NAVER_REDIRECT_URI = os.getenv('NAVER_REDIRECT_URI')
ENCODED_REDIRECT_URI = urllib.parse.quote(NAVER_REDIRECT_URI, safe="")  # URL 인코딩 적용
ALGORITHM = "HS256"

# 네이버 인증 URL 생성
def get_naver_auth_url(state: str):
    return (
        "https://nid.naver.com/oauth2.0/authorize"
        "?response_type=code"
        f"&client_id={NAVER_LOGIN_CLIENT_ID}"
        f"&redirect_uri={NAVER_REDIRECT_URI}"
        f"&state={state}"
    )

# 네이버 토큰 요청
async def get_naver_token(code: str, state: str):
    try:
        token_url = "https://nid.naver.com/oauth2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {
            "grant_type": "authorization_code",
            "client_id": NAVER_LOGIN_CLIENT_ID,
            "client_secret": NAVER_LOGIN_CLIENT_SECRET,
            "code": code,
            "state": state
        }
        
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(token_url, headers=headers, data=params)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP error: {e.response.status_code}"}
    except httpx.ConnectTimeout:
        print("Connection timeout error")
        return {"error": "Connection timeout"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": "Unexpected error"}

# 네이버 사용자 정보 요청
async def get_naver_user_info(access_token: str):
    user_info_url = "https://openapi.naver.com/v1/nid/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(user_info_url, headers=headers)
        response.raise_for_status()
        return response.json()

@router.get("/login/naver", response_class=RedirectResponse)
async def login_naver():
    state = secrets.token_urlsafe(32)
    login_url = get_naver_auth_url(state=state)
    return RedirectResponse(url=login_url)

@router.get("/api/login/naverOAuth")
async def naver_callback(code: str, state: str, db: Session = Depends(get_mysql_db)):
    """네이버에서 받은 code로 access token 요청"""
    
    token_data = await get_naver_token(code, state)
    print(token_data)

    if "access_token" not in token_data:
        return {"error": "토큰 발급 실패", "response": token_data}
    
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]

    # 토큰을 사용하여 네이버 사용자 정보 요청
    user_info = await get_naver_user_info(access_token)
    print(user_info)
    
    if "response" not in user_info:
        return {"error": "사용자 정보 조회 실패", "response": user_info}
    
    user_id = user_info["response"]["id"]  # 네이버 유저 고유 ID

    # DB에서 user_id가 존재하는지 확인
    existing_user = read_user(db, user_id)
    print(f"existing_user : {existing_user}")

    if not existing_user:
        # 신규 유저 등록
        user_data = {
            "user_id": user_id,
            "name": user_info["response"]["name"],
            "birth_year": user_info["response"]["birthyear"],
            "gender": user_info["response"]["gender"],
            "phone_number": user_info["response"].get("mobile"),  
            "email": user_info["response"].get("email")  
        }
        user_data = {key: value for key, value in user_data.items() if value is not None}
        create_user(db, user_data)

    existing_token = read_token(db, user_id)
    print(f"existing token : {existing_token}")

    if not existing_token:
        # Tokens 테이블에 refresh_token 저장
        token_data = {
            "user_id": user_id,
            "refresh_token": refresh_token
        }
        create_token(db, token_data)
    
    return {"message": "로그인 성공", "user_id": user_id, "access_token": access_token}

    # 프론트에 정보 바로 넘기는게 아니라 jwt 토큰 발급
    # JWT 토큰 생성
    # access_token = create_access_token(data=디비에서 뽑은데이터)
    # refresh_token = create_refresh_token(data=디비에서 뽑은데이터)
    # return {
    #     "access_token": access_token,
    #     "refresh_token": refresh_token,
    #     "token_type": "bearer"
    # }
    # 이제 리프래시 토큰과 액세스 토큰을 만들어 프론트 주고 프론트가 토큰 잘 주면 나는 ㅇㅋ 하면서 로그인 그대로 ㅇㅇ 해주고~ 그런 것!
    
    # return user_info # 프론트에 사용자 정보만 줌

    # 프론트는 이제 헤더에 저 jwt 토큰을 넣어서 주고 받아야함
    # 그럼 그걸 여기서 검증해야 함
    '''from fastapi import Depends, HTTPException, Security
    from fastapi.security import OAuth2PasswordBearer
    from jose import jwt, JWTError

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def verify_token(token: str = Security(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
            
    
    @router.get("/api/protected")
    def protected_route(token_data: dict = Depends(verify_token)):
        return {"message": "인증된 사용자만 접근 가능", "user": token_data}'''
    

    # 리프래시 토큰으로 뉴 액세스 토큰 
    '''
    @router.post("/auth/refresh")
    def refresh_access_token(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            new_access_token = create_access_token(data={"sub": payload["sub"]}, expires_delta=timedelta(minutes=60))
            return {"access_token": new_access_token, "token_type": "bearer"}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")'''
