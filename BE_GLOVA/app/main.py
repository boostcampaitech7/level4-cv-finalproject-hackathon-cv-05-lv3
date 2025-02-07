from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from database.connections import init_db  
from database.config import get_db_status  # ✅ DB 상태 조회 함수 추가
import os
from dotenv import load_dotenv
from apis import home, badge, books, realhome, login

load_dotenv()
SESSIONMIDDLEWARE_SECRET_KEY=os.getenv('SESSIONMIDDLEWARE_SECRET_KEY')
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key=SESSIONMIDDLEWARE_SECRET_KEY)  # openssl rand -hex 32로 임의 생성

# API 라우트 추가
app.include_router(login.router)
app.include_router(home.router)
app.include_router(books.router)
app.include_router(badge.router)
app.include_router(realhome.router)

@app.on_event("startup")  # FastAPI 실행 시 DB 초기화 실행
def startup_event():
    init_db()  # 테이블이 없으면 생성

@app.get("/")
def read_root():
    return {"message": "하이퍼글로바 준비 완료"}

# DB 상태 확인 API 추가
@app.get("/db-status")
def db_status():
    return get_db_status()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
