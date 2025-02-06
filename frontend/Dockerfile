# (1) Node 22 (가정) - 실제 Docker Hub에 해당 태그가 없을 수 있으므로 주의
FROM node:22.13.1

# (2) 작업 디렉토리
WORKDIR /app
RUN apt-get update && apt-get install -y curl
# (3) 의존성 설치
COPY package*.json ./
RUN npm install

# (4) 소스 복사
COPY . .

# (5) Vite 기본 dev 서버 포트
EXPOSE 3000

# (6) 개발 서버 실행
CMD ["npm", "run", "dev"]
