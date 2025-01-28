FROM python:3.9-slim

WORKDIR /app

# FastAPI 등 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 백엔드 소스 복사
COPY . .

# uvicorn 포트
EXPOSE 8000

ENV PYTHONPATH=/app
# 개발 모드 (auto-reload)
CMD ["uvicorn", "BE_GLOVA.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
