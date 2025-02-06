# CUDA 12.2가 포함된 Ubuntu 20.04 기반 이미지 사용
FROM nvidia/cuda:12.2.2-devel-ubuntu20.04

# noninteractive 모드 설정
ENV DEBIAN_FRONTEND=noninteractive

# 필수 패키지 및 Python 3.10 설치 준비
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      software-properties-common \
      curl && \
    # tzdata의 시간대 설정 자동화 (Asia/Seoul로 설정)
    echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/Asia select Seoul" | debconf-set-selections && \
    apt-get install -y --no-install-recommends tzdata && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
      python3.10 \
      python3.10-venv \
      python3.10-distutils && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    ln -s /usr/bin/python3.10 /usr/bin/python && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 별도로 PyTorch 관련 패키지 설치
RUN pip install --default-timeout=300 torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# requirements.txt 파일 복사 및 기본 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 애플리케이션 소스 복사
COPY . .

EXPOSE 8000
COPY ./sdxl_img2img.py /workspace/sdxl_img2img.py
COPY ./badgemkrsdxl.safetensors /workspace/badgemkrsdxl.safetensors
COPY ./test01.jpg /workspace/test01.jpg
ENV PYTHONPATH=/app

CMD ["uvicorn", "BE_GLOVA.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
