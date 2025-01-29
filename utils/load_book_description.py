import os
import ssl
import urllib.request
import json
import time
import pandas as pd
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# SSL 인증서 검증 비활성화
ssl._create_default_https_context = ssl._create_unverified_context

# 환경 변수 읽기
client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')

# 책 검색 API 호출 함수
def fetch_book_details_async(book_title: str, retries=3, delay=5):
    encText = urllib.parse.quote(book_title)
    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    
    for attempt in range(retries):
        try:
            response = urllib.request.urlopen(request, timeout=10)  # 타임아웃 설정
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read()
                return json.loads(response_body.decode('utf-8'))
            else:
                print(f"Error Code: {rescode}")
                return None
        except urllib.error.URLError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)  # 재시도 전 대기
    print("All retries failed.")
    return None

# CSV 파일 읽기
file_path = '사서추천도서목록_utf8.csv'
book_data = pd.read_csv(file_path)

books_info = book_data[['카테고리', '서브 카테고리', '서명', '저자']]
# 새로운 컬럼 추가를 위한 리스트 초기화
descriptions = []
cache = {}

# 책 정보 순회
for idx, row in books_info.iterrows():
    book_title = row['서명']
    author_name = row['저자']

    # 캐시에 데이터가 있는지 확인
    if book_title in cache:
        result = cache[book_title]
    else:
        result = fetch_book_details_async(book_title)
        cache[book_title] = result  # 캐시에 저장

    # 검색 결과 처리
    if result and 'items' in result and len(result['items']) > 0:
        found_description = ""  # 초기값 설정
        for item in result['items']:
            # 저자 이름이 포함된 경우 설명 추가
            if author_name.strip() in item['author']:
                found_description = item['description']
                break
        descriptions.append(found_description)
    else:
        descriptions.append("")  # 검색 결과가 없을 경우 빈 값 추가

    # 중간 결과 저장
    if (idx + 1) % 10 == 0 or (idx + 1) == len(books_info):  # 10번마다 저장
        # 현재까지의 데이터프레임 업데이트
        books_info.loc[:idx, '책 설명'] = descriptions
        books_info.to_csv("books_with_descriptions_partial.csv", index=False, encoding='utf-8')
        print(f"Saved {idx + 1}/{len(books_info)} rows to books_with_descriptions_partial.csv")

    # 요청 간 1초 지연
    time.sleep(1)

# 최종 결과 저장
books_info['책 설명'] = descriptions
books_info.to_csv("books_with_descriptions.csv", index=False, encoding='utf-8')
print("All data saved to books_with_descriptions.csv")


