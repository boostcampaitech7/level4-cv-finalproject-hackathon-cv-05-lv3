import os
import requests
import time
from PIL import Image, ImageChops
from io import BytesIO

# 🔑 네이버 API 키 (본인 API 키 입력)
NAVER_CLIENT_ID = "wJWKLF_qgh3mFYWWzWW2"
NAVER_CLIENT_SECRET = "B0HkoLa_rE"

# 📌 더미 이미지 파일 2개 (사용자가 업로드한 이미지)
DUMMY_IMAGE_PATHS = ["/data/ephemeral/home/level4-cv-finalproject-hackathon-cv-05-lv3/dataset/dump1.jpg", "/data/ephemeral/home/level4-cv-finalproject-hackathon-cv-05-lv3/dataset/dump2.jpg"]  # 더미 이미지 경로 2개
DUMMY_IMAGES = [Image.open(path) for path in DUMMY_IMAGE_PATHS]  # 더미 이미지 로드

# 저장할 폴더 만들기
SAVE_DIR = "source_images"
os.makedirs(SAVE_DIR, exist_ok=True)

# 검색할 출판 연도 범위 설정 (2024년부터 2015년까지)
YEARS = list(range(2024, 2000, -1))  # 2024년부터 2015년까지 검색

# ❌ 제외할 자격증 관련 키워드 리스트
EXCLUDED_KEYWORDS = ["기능사","모의고사","기출","자격증", "토익", "토플", "시험", "한국사", "공무원", "기출", "NCS", "검정고시", "회계", "세무사", "전산", "기술사", "기사", "운전면허"]

def is_dummy_image(image_url):
    """다운로드한 이미지가 2개의 더미 이미지 중 하나와 동일한지 비교"""
    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            return False

        image = Image.open(BytesIO(response.content))

        # 모든 더미 이미지와 비교
        for dummy in DUMMY_IMAGES:
            image_resized = image.resize(dummy.size)  # 크기 맞춤
            diff = ImageChops.difference(image_resized, dummy)

            # 이미지가 완전히 동일하면 제외
            if not diff.getbbox():
                print(f"🚫 더미 이미지와 동일 → 제외: {image_url}")
                return True

    except Exception as e:
        print(f"이미지 비교 오류: {e}")
    
    return False

def get_naver_book_covers(year, start=1, display=100):
    """네이버 책 API에서 특정 연도의 한국어 책 표지를 가져오는 함수 (자격증 & 더미 이미지 제외)"""
    url = "https://openapi.naver.com/v1/search/book.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {
        "query": f"{year}",  # 📌 출판 연도 검색
        "display": display,  # 한 번에 가져올 책 개수 (최대 100)
        "start": start,  # 시작 위치
        "sort": "date",  # 최신순 정렬
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"API 요청 실패: {response.status_code}")
        return []
    
    data = response.json()
    books = data.get("items", [])

    covers = []
    for book in books:
        title = book.get("title", "")
        cover_url = book.get("image")

        # ❌ 제목에 자격증 관련 키워드가 포함된 경우 제외
        if any(keyword in title for keyword in EXCLUDED_KEYWORDS):
            print(f"🚫 제외된 책: {title}")
            continue

        # ✅ 다운로드할 이미지가 '이미지 준비 중'인지 검사
        if cover_url and not is_dummy_image(cover_url):
            covers.append(cover_url)
    
    return covers

def download_naver_book_covers(num_images=10000):
    """네이버 책 API에서 표지를 num_images개 다운로드하는 함수 (자격증 & 더미 이미지 제외)"""
    downloaded = 0

    for year in YEARS:  # 📌 출판 연도별 검색 (2024 ~ 2015)
        start = 1  # API는 1부터 시작

        while downloaded < num_images:
            # API에서 표지 가져오기
            cover_urls = get_naver_book_covers(year, start=start, display=100)
            
            if not cover_urls:
                print(f"📌 {year}년의 모든 검색 결과를 가져왔습니다. 다음 연도로 이동합니다.")
                break  # 다음 연도로 이동
            
            for cover_url in cover_urls:
                if downloaded >= num_images:
                    break
                
                # 이미지 다운로드
                save_path = os.path.join(SAVE_DIR, f"book{downloaded+1}.jpg")
                cover_response = requests.get(cover_url)
                
                if cover_response.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(cover_response.content)
                    print(f"[{downloaded+1}/{num_images}] 다운로드 완료: {save_path}")
                    downloaded += 1
                else:
                    print(f"이미지 다운로드 실패: {cover_url}")

                time.sleep(0.1)  # API 요청 간격 조정

            # API start 값 증가 (100개씩 검색)
            start += 100

        if downloaded >= num_images:
            break  # 10,000개 다운로드 완료 시 종료

    print(f"✅ 다운로드 완료! 총 {downloaded}장의 책 표지를 저장했습니다.")

if __name__ == "__main__":
    download_naver_book_covers()
