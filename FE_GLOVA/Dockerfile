FROM node:22.13.1

# 작업 디렉터리 설정
WORKDIR /app

# OpenVPN 설치
RUN apt-get update && apt-get install -y openvpn

# 의존성 설치
COPY package*.json ./
RUN npm install

# 애플리케이션 소스 복사
COPY . .

EXPOSE 3000

# 컨테이너 시작 시 entrypoint 스크립트 실행
ENTRYPOINT ["/entrypoint.sh"]

