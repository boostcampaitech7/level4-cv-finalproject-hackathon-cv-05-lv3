# # CUDA 12.2가 포함된 Ubuntu 22.04 기반 이미지 사용
# FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

# # 비대화형 모드 설정
# ENV DEBIAN_FRONTEND=noninteractive

# # 필수 패키지 및 Python 3.10, 빌드 도구, LLVM 14 설치 준비
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#       software-properties-common \
#       curl \
#       openvpn \
#       openssh-client \
#       iputils-ping \
#       tzdata && \
#     # 시간대 설정 (Asia/Seoul)
#     echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && \
#     echo "tzdata tzdata/Zones/Asia select Seoul" | debconf-set-selections && \
#     # deadsnakes PPA 추가 및 Python 3.10 관련 패키지 설치
#     add-apt-repository ppa:deadsnakes/ppa && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends \
#       python3.10 \
#       python3.10-venv \
#       python3.10-distutils \
#       python3.10-dev \
#       build-essential \
#       llvm-14-dev \
#       libffi-dev \
#       postgresql-client \
#       mysql-client && \
#     # pip 설치 (최신 버전 사용)
#     curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
#     ln -s /usr/bin/python3.10 /usr/bin/python && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*

# # 작업 디렉터리 설정
# WORKDIR /app

# # PyTorch (CUDA 지원) 등 필요한 패키지 설치
# RUN pip install --default-timeout=300 \
#       torch==2.5.1 \
#       torchvision==0.20.1 \
#       torchaudio==2.5.1 \
#       --index-url https://download.pytorch.org/whl/cu121

# # LLVM 14 관련 설정: llvmlite가 llvm-config-14를 사용하도록 환경변수 설정
# ENV LLVM_CONFIG=/usr/bin/llvm-config-14

# # 최신 pip로 업데이트
# RUN pip install --upgrade pip

# # 최신 numba와 llvmlite (LLVM 14 지원 버전) 미리 설치
# RUN pip install --no-cache-dir numba==0.57.0 llvmlite==0.40.0

# # requirements.txt 파일 복사 및 나머지 패키지 설치
# # → 여기서 requirements.txt에서는 numba와 llvmlite 관련 항목은 제거되어 있어야 합니다.
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # 애플리케이션 소스 전체 복사
# COPY . .

# # 추가 파일 복사 (예: 모델 체크포인트 등)
# COPY ./badgemkrsdxl.safetensors /workspace/badgemkrsdxl.safetensors
# # 필요시 다른 파일들도 복사 가능
# # COPY ./test01.jpg /workspace/test01.jpg

# # PYTHONPATH 설정 (애플리케이션 모듈 검색 경로)
# ENV PYTHONPATH=/app

# # --- OpenVPN 및 SSH 관련 설정 ---
# RUN mkdir -p /etc/openvpn /etc/ssh

# # OpenVPN 설정 파일 및 인증 정보 복사
# COPY openvpn01-TCP4-1188-config.ovpn /etc/openvpn/config.ovpn
# COPY credentials.txt /etc/openvpn/credentials.txt

# # PEM 키 복사 및 권한 설정
# COPY beomjoismoving.pem /etc/ssh/beomjoismoving.pem
# RUN chmod 600 /etc/ssh/beomjoismoving.pem

# # entrypoint 스크립트 복사 및 실행 권한 부여
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# # 애플리케이션 포트 노출
# EXPOSE 8000

# # 컨테이너 시작 시 entrypoint 스크립트 실행 후 CMD 실행
# ENTRYPOINT ["/entrypoint.sh"]
# CMD ["uvicorn", "BE_GLOVA.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CUDA 12.2가 포함된 Ubuntu 22.04 기반 이미지 사용
FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

# 비대화형 모드 설정
ENV DEBIAN_FRONTEND=noninteractive

# 필수 패키지 및 Python 3.10, 빌드 도구, LLVM 14 설치 준비
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      software-properties-common \
      curl \
      openvpn \
      openssh-client \
      iputils-ping \
      tzdata && \
    # 시간대 설정 (Asia/Seoul)
    echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/Asia select Seoul" | debconf-set-selections && \
    # deadsnakes PPA 추가 및 Python 3.10 관련 패키지 설치
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
      python3.10 \
      python3.10-venv \
      python3.10-distutils \
      python3.10-dev \
      build-essential \
      llvm-14-dev \
      libffi-dev \
      postgresql-client \
      mysql-client && \
    # pip 설치 (최신 버전 사용)
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    ln -s /usr/bin/python3.10 /usr/bin/python && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 작업 디렉터리 설정
WORKDIR /app

# PyTorch (CUDA 지원) 등 필요한 패키지 설치
RUN pip install --default-timeout=300 \
      torch==2.5.1 \
      torchvision==0.20.1 \
      torchaudio==2.5.1 \
      --index-url https://download.pytorch.org/whl/cu121

# LLVM 14 관련 설정: llvmlite가 llvm-config-14를 사용하도록 환경변수 설정
ENV LLVM_CONFIG=/usr/bin/llvm-config-14

# 최신 pip로 업데이트
RUN pip install --upgrade pip

# 최신 numba와 llvmlite (LLVM 14 지원 버전) 미리 설치
RUN pip install --no-cache-dir numba==0.57.0 llvmlite==0.40.0

# requirements.txt 파일 복사 및 나머지 패키지 설치
# → 여기서 requirements.txt에서는 numba와 llvmlite 관련 항목은 제거되어 있어야 합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 전체 복사
COPY . .

# 추가 파일 복사 (예: 모델 체크포인트 등)
COPY ./badgemkrsdxl.safetensors /workspace/badgemkrsdxl.safetensors
# 필요시 다른 파일들도 복사 가능
# COPY ./test01.jpg /workspace/test01.jpg

# PYTHONPATH 설정 (애플리케이션 모듈 검색 경로)
ENV PYTHONPATH=/app

# --- OpenVPN 및 SSH 관련 설정 ---
RUN mkdir -p /etc/openvpn /etc/ssh

# OpenVPN 설정 파일 및 인증 정보 복사
COPY openvpn01-TCP4-1188-config.ovpn /etc/openvpn/config.ovpn
COPY credentials.txt /etc/openvpn/credentials.txt

# PEM 키 복사 및 권한 설정
COPY beomjoismoving.pem /etc/ssh/beomjoismoving.pem
RUN chmod 600 /etc/ssh/beomjoismoving.pem

# === SSL 인증서 추가 (HTTPS 설정) ===
# 빌드 컨텍스트에 mkcert 등으로 생성한 인증서 파일 (localhost.pem, localhost-key.pem)이 있어야 합니다.
RUN mkdir -p /etc/ssl/certs /etc/ssl/private
COPY localhost.pem /etc/ssl/certs/localhost.pem
COPY localhost-key.pem /etc/ssl/private/localhost-key.pem
RUN chmod 644 /etc/ssl/certs/localhost.pem && \
    chmod 600 /etc/ssl/private/localhost-key.pem

# entrypoint 스크립트 복사 및 실행 권한 부여
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 애플리케이션 포트 노출
EXPOSE 8000

# 컨테이너 시작 시 entrypoint 스크립트 실행 후 CMD 실행
ENTRYPOINT ["/entrypoint.sh"]

# uvicorn 실행 시 SSL 옵션 추가 (HTTPS)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--ssl-keyfile", "/etc/ssl/private/localhost-key.pem", "--ssl-certfile", "/etc/ssl/certs/localhost.pem"]
