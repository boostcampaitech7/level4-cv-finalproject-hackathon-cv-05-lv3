from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import secrets

from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 환경 변수 로드
load_dotenv()

# 환경 변수
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
_state = secrets.token_urlsafe(16)  # CSRF 방지용 랜덤 문자열
# 나중에 Redis를 사용하면 분산 서버에서도 안전하게 state를 저장하고 검증할 수 있어.
app = FastAPI()

# 네이버 인증 URL 생성
def get_naver_auth_url(state: str):
    return (
        "https://nid.naver.com/oauth2.0/authorize"
        "?response_type=code"
        f"&client_id={NAVER_CLIENT_ID}"
        "&redirect_uri=http://localhost:8000/callback"
        f"&state={state}"
    )

# 네이버 토큰 요청
async def get_naver_token(code: str, state: str):
    token_url = "https://nid.naver.com/oauth2.0/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "grant_type": "authorization_code",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "code": code,
        "state": state
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=params)
        response.raise_for_status()
        return response.json()

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


@app.get("/")
async def root():
    # 1. 사용자를 네이버 OAuth 페이지로 리디렉션
    
    auth_url = get_naver_auth_url(_state)
    # 이걸 프론트에서 호출하면 네이버 로그인 페이지로 이동하는 URL을 받는 것 
    return RedirectResponse(auth_url)

# 이 담에 사용자가 네이버 로그인 동의하면 네이버는 code랑 state를 벡엔드로 넘김. 서버가 이걸 받아서 네이버한테 액세스 토큰을 요청해야 함 
@app.get("/callback")
async def callback(request: Request):
    # 네이버가 나에게 준 code/state 
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    
    if state != _state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    # 네이버에서 발급된 액세스 토큰을 요청
    token_response = await get_naver_token(code, state)
    access_token = token_response.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to get access token")

    # 액세스 토큰을 사용하여 사용자 정보를 요청
    user_info_data = await get_naver_user_info(access_token)
    print(user_info_data)
    if "response" not in user_info_data:
        raise HTTPException(status_code=400, detail="네이버 사용자 정보 조회 실패")

    user_info = user_info_data["response"]
    print(user_info['name'])

    # =======================================================
    # 디비 저장?
    # db_user = db.query(User).filter(User.naver_id == user_info["id"]).first()

    # if not db_user:
    #     new_user = User(naver_id=user_info["id"], email=user_info["email"], nickname=user_info["nickname"])
    #     db.add(new_user)
    #     db.commit()
    #     db.refresh(new_user)
    #     db_user = new_user

    # 프론트에 정보 바로 넘기는게 아니라 jwt 토큰 발급
    # JWT 토큰 생성
    access_token = create_access_token(data=디비에서 뽑은데이터)
    refresh_token = create_refresh_token(data=디비에서 뽑은데이터)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
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
            
    
    @app.get("/api/protected")
    def protected_route(token_data: dict = Depends(verify_token)):
        return {"message": "인증된 사용자만 접근 가능", "user": token_data}'''
    

    # 리프래시 토큰으로 뉴 액세스 토큰 
    '''
    @app.post("/auth/refresh")
    def refresh_access_token(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            new_access_token = create_access_token(data={"sub": payload["sub"]}, expires_delta=timedelta(minutes=60))
            return {"access_token": new_access_token, "token_type": "bearer"}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")'''


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run("lo:app", host="0.0.0.0", port=8000, reload=True)