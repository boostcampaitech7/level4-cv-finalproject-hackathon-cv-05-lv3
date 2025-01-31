import os
import requests

# 다운로드할 URL 목록
urls = [
    "https://c.animaapp.com/MmL976K3/img/line-4.svg"
]

# 저장 디렉토리 설정
output_dir = "anima_images"
os.makedirs(output_dir, exist_ok=True)

# 파일 다운로드
for url in urls:
    file_name = os.path.basename(url)  # URL에서 파일 이름 추출
    file_path = os.path.join(output_dir, file_name)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 요청 오류 확인
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

print(f"All files downloaded to '{output_dir}'")
