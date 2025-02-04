from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from apis import home, badge, books

load_dotenv()
SESSIONMIDDLEWARE_SECRET_KEY=os.getenv('SESSIONMIDDLEWARE_SECRET_KEY')
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    # allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key=f"Bearer {SESSIONMIDDLEWARE_SECRET_KEY}" ) # openssl rand -hex 32로 임의 생성

# API 라우트 추가
app.include_router(home.router)
app.include_router(books.router)
app.include_router(badge.router)

@app.get("/")
def read_root():
    return {"message": "하이퍼글로바 준비 완료"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
