from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# .env 파일 로드
load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

app = FastAPI()

# CORS 설정 (React에서 요청 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱의 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 바디 형식 정의
class NaverTokenRequest(BaseModel):
    code: str
    state: str

@app.post("/api/naver/token")
def get_naver_token(request: NaverTokenRequest):
    """ 네이버 OAuth 토큰 요청 API """
    if not request.code or not request.state:
        raise HTTPException(status_code=400, detail="Code 또는 State 값이 없습니다.")

    token_url = "https://nid.naver.com/oauth2.0/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "code": request.code,
        "state": request.state,
    }

    response = requests.post(token_url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="네이버 토큰 요청 실패")

    return response.json()  # 네이버에서 받은 토큰 응답을 그대로 반환