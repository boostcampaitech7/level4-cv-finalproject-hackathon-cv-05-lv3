from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router 

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우트 추가
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "하이퍼글로바 준비 완료"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
