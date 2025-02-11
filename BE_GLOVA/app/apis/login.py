from fastapi import Request, Response, Depends, HTTPException, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
import os
import urllib.parse
import secrets
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ..database.crud import read_user, create_user, read_token, create_token
from ..database.connections import get_mysql_db

router = APIRouter()

# 환경 변수 로드
load_dotenv()

# 환경 변수 설정
NAVER_LOGIN_CLIENT_ID = os.getenv('NAVER_LOGIN_CLIENT_ID')
NAVER_LOGIN_CLIENT_SECRET = os.getenv('NAVER_LOGIN_CLIENT_SECRET')
NAVER_REDIRECT_URI = os.getenv('NAVER_REDIRECT_URI')
ENCODED_REDIRECT_URI = urllib.parse.quote(NAVER_REDIRECT_URI, safe="")
FRONTEND_URL = os.getenv("FRONTEND_URL")
ALGORITHM = "HS256"

# JWT access_token 생성 함수
def create_access_token(data: dict, expires_in: int):
    """ 주어진 데이터와 만료 시간으로 JWT Access Token 생성 """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=int(expires_in))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, NAVER_LOGIN_CLIENT_SECRET, algorithm=ALGORITHM)

# 네이버 인증 URL 생성
def get_naver_auth_url(state: str):
    return (
        "https://nid.naver.com/oauth2.0/authorize"
        "?response_type=code"
        f"&client_id={NAVER_LOGIN_CLIENT_ID}"
        f"&redirect_uri={NAVER_REDIRECT_URI}"
        f"&state={state}"
    )

# 네이버 OAuth 토큰 요청
async def get_naver_token(code: str, state: str):
    try:
        token_url = "https://nid.naver.com/oauth2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {
            "grant_type": "authorization_code",
            "client_id": NAVER_LOGIN_CLIENT_ID,
            "client_secret": NAVER_LOGIN_CLIENT_SECRET,
            "code": code,
            "state": state,
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

# 네이버 OAuth 토큰 요청 처리
async def handle_naver_oauth(code: str, state: str):
    token_data = await get_naver_token(code, state)
    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail={"error": "토큰 발급 실패", "response": token_data})
    return token_data["access_token"], token_data["refresh_token"], token_data["expires_in"]

# 네이버 사용자 정보 요청
async def get_naver_user_info(access_token: str):
    user_info_url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(user_info_url, headers=headers)
        response.raise_for_status()
        return response.json()

# 사용자 정보 처리 및 DB 저장
async def handle_user_data(db: Session, access_token: str):
    user_info = await get_naver_user_info(access_token)
    if "response" not in user_info:
        raise HTTPException(status_code=400, detail={"error": "사용자 정보 조회 실패", "response": user_info})
    
    user_id = user_info["response"]["id"]
    existing_user = read_user(db, user_id)
    
    if not existing_user:
        user_data = {
            "user_id": user_id,
            "birth_year": user_info["response"].get("birthyear"),
            "gender": user_info["response"].get("gender"),
        }
        user_data = {key: value for key, value in user_data.items() if value is not None}
        create_user(db, user_data)
    return user_id

# refresh token 저장 및 JWT 발급
async def handle_token_data(db: Session, user_id: str, refresh_token: str, expires_in: int):
    existing_token = read_token(db, user_id)
    if not existing_token:
        create_token(db, {"user_id": user_id, "refresh_token": refresh_token})
    return create_access_token(data={"sub": user_id}, expires_in=expires_in)

@router.get("/login/naver", response_class=RedirectResponse)
async def login_naver():
    state = secrets.token_urlsafe(32)
    login_url = get_naver_auth_url(state=state)
    return RedirectResponse(url=login_url)

@router.get("/api/login/naverOAuth")
async def naver_callback(response: Response, code: str, state: str, db: Session = Depends(get_mysql_db)):
    access_token, refresh_token, expires_in = await handle_naver_oauth(code, state)
    print(f"access_token : {access_token}, refresh_token: {refresh_token}, expires_in : {expires_in}")
    user_id = await handle_user_data(db, access_token)
    jwt_access_token = await handle_token_data(db, user_id, refresh_token, expires_in)
    
    response = RedirectResponse(url=f"{FRONTEND_URL}/Home")
    response.set_cookie(
        key="access_token",
        value=jwt_access_token,
        httponly=False,
        secure=False,
        samesite="None",
        path="/",
        max_age=expires_in
    )
    print("쿠키 설정 완료!")
    return response

# JWT 토큰 검증 함수
def verify_access_token(token: str, db: Session):
    """ JWT 토큰을 검증하고, user_id가 DB에 존재하는지 확인 """
    try:
        payload = jwt.decode(token, NAVER_LOGIN_CLIENT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        # 🔹 DB에서 user_id 확인
        user = read_user(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User does not exist")

        return user_id  # 유효한 user_id만 반환

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 자동 로그인 체크 API
@router.get("/api/check-auth")
def check_auth(request: Request, db: Session = Depends(get_mysql_db)):
    """
    - 쿠키에 access_token이 있는지 확인
    - access_token이 있으면 검증 후 user_id 반환
    - 없으면 401 Unauthorized 응답
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")  # 쿠키가 삭제된 경우
    
    # 네이버 API로 access_token 유효성 확인
    if not is_access_token_valid(access_token):
        raise HTTPException(status_code=401, detail="Access token is expired")  # 만료된 경우

    user_id = verify_access_token(access_token, db)  # JWT 검증 및 DB 유저 확인
    return {"user_id": user_id, "message": "인증 성공"}

# @router.get("/api/check-auth")
# async def check_auth(request: Request, db: Session = Depends(get_mysql_db)):
#     access_token = request.cookies.get("access_token")
#     if not access_token:
#         raise HTTPException(status_code=401, detail="Access token is missing")
    
#     # 네이버 API 검증 대신 자체 JWT 검증만 수행
#     try:
#         user_id = verify_access_token(access_token, db)
#     except HTTPException as e:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
    
#     return {"user_id": user_id, "message": "인증 성공"}


# 네이버 Access Token 유효성 체크
async def is_access_token_valid(access_token: str):
    """
    네이버 API를 사용하여 access_token이 유효한지 확인하는 함수
    """
    url = "https://openapi.naver.com/v1/nid/verify"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()

    # resultcode가 '00'이면 유효한 access_token
    return data.get("resultcode") == "00"

# Refresh Token을 이용하여 Access Token 재발급
async def request_new_access_token(refresh_token: str):
    """
    네이버 OAuth API를 사용하여 refresh_token으로 새로운 access_token 발급 요청
    """
    url = "https://nid.naver.com/oauth2.0/token"
    params = {
        "grant_type": "refresh_token",
        "client_id": NAVER_LOGIN_CLIENT_ID,
        "client_secret": NAVER_LOGIN_CLIENT_SECRET,
        "refresh_token": refresh_token,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        return None  # 오류 발생 시 None 반환

    return response.json()

# Access Token이 만료된 경우, Refresh Token으로 재발급하는 API
@router.get("/api/refresh-token")
async def refresh_access_token(request: Request, response: Response, db: Session = Depends(get_mysql_db)):
    """
    - 현재 access_token이 유효한지 검사
    - 만료되었을 경우, refresh_token을 사용하여 새로운 access_token 발급
    - 재발급 성공 시, 새로운 access_token을 쿠키에 저장
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")  # 쿠키에 access_token이 없는 경우
    
    # access_token이 유효한지 네이버 API로 확인
    if await is_access_token_valid(access_token):
        return {"message": "Access token is still valid"}  # 유효하면 새로 발급할 필요 없음
    
    try:
        payload = jwt.decode(access_token, NAVER_LOGIN_CLIENT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")  # JWT가 유효하지 않음

    # DB에서 refresh_token 조회
    stored_token = read_token(db, user_id)
    if not stored_token:
        raise HTTPException(status_code=401, detail="Refresh token not found or expired")  # Refresh Token이 없으면 인증 실패

    refresh_token = stored_token.refresh_token

    # 네이버 API를 통해 새로운 access_token 요청
    new_token_data = await request_new_access_token(refresh_token)
    if not new_token_data or "access_token" not in new_token_data:
        raise HTTPException(status_code=401, detail="Failed to refresh access token")  # 재발급 실패

    # 새로운 access_token 정보
    new_access_token = new_token_data["access_token"]

    # 쿠키에 새로운 access_token 저장
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=False,
        secure=False,
        samesite="None",
        path="/",
        max_age=3600
    )

    return {"message": "Access token refreshed successfully"}

# 로그아웃 API (쿠키 삭제)
@router.post("/api/logout")
async def logout(response: Response):
    """
    - 로그아웃 시 쿠키에서 access_token과 refresh_token 제거
    """
    response.delete_cookie("access_token")
    return JSONResponse(content={"message": "Logged out successfully"}, status_code=200)

