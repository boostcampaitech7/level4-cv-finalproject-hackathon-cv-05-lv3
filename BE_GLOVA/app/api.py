from fastapi import FastAPI, HTTPException, Request, APIRouter, File, UploadFile, BackgroundTasks
from dotenv import load_dotenv
import requests
import os
import json
import re
from schemas import UserQuestion, ClovaResponse, CalendarResponse, BadgeRequest, BadgeResponse
from random import randint
import datetime
from typing import List, Dict
import base64
from pathlib import Path
import zipfile
from fastapi.responses import FileResponse
from model import generate_badge

router = APIRouter() # 모든 엔드포인트를 이 router에 정의하고, main에서 한 번에 추가 

load_dotenv()

# 임시 테스트 앱 CLOVA_REQUEST_ID, 실제 서비스와 연동 시 변경되므로 .env에서 변경!
# CLOVA API1 설정정
CLOVA_API_URL = os.getenv('CLOVA_API_URL')
CLOVA_API_KEY = os.getenv('CLOVA_Authorization')
CLOVA_REQUEST_ID = os.getenv('CLOVA_REQUEST_ID') 
# Clova API2 설정
CLOVA_API2_URL = os.getenv('CLOVA_API2_URL')
CLOVA_REQUEST_ID2 = os.getenv('CLOVA_REQUEST_ID2')
# 환경변수 확인
if not (CLOVA_API_KEY or CLOVA_API_URL or CLOVA_REQUEST_ID or CLOVA_API2_URL or CLOVA_REQUEST_ID2):
    raise ValueError("CLOVA 환경 변수가 설정되지 않았습니다.")


# 클로바 api1 호출
# 서버에 정보를 보내고, 결과를 받아옴 
@router.post("/api/home")
async def save_question(user_question: UserQuestion):
    class CompletionExecutor:
        def __init__(self, api_url, api_key, request_id):
            self._api_url = api_url
            self._api_key = api_key
            self._request_id = request_id

        def execute(self, completion_request):
            headers = {
                'Authorization': self._api_key,
                'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'text/event-stream'
            }
            try:
                with requests.post(self._api_url,
                                headers=headers, json=completion_request, stream=True) as r:
                    r.raise_for_status()  # HTTP 에러 발생 시 예외 처리
                    response_data = []
                    for line in r.iter_lines():
                        if line:
                            response_data.append(line.decode("utf-8"))
                    return response_data
            except requests.RequestException as e:
                raise HTTPException(status_code=500, detail=f"Error during Clova API call: {str(e)}")


    try:
        # Clova API 설정
        completion_executor = CompletionExecutor(
            api_url=f"{CLOVA_API_URL}",
            api_key=f"Bearer {CLOVA_API_KEY}",
            request_id=CLOVA_REQUEST_ID
        )
    
        preset_text = [
            {"role": "system", "content": (
                "- 당신은 재치있는 도서 큐레이터입니다.\n"
                f"- 사용자의 나이: {user_question.age}, 성별: {user_question.gender}\n"
                "- 사용자의 질문에 대해 사용자의 나이, 성별을 분석하여 시중에 있는 책에서 관련 내용을 인용하거나 추천하는 방식으로 답변합니다.\n"
                "- 사용자의 질의를 분석하고 질의와 상관관계를 보이는 책 제목으로 답해줘\n"
                "- 1개의 답변이고, 명확하고 간결하며, 독자가 흥미를 느낄 수 있도록 작성하세요.\n\n"
                "예시:\n질문: 아픈 건 싫어!\n답변: [아픈 건 싫으니까 방어력에 올인하려고 합니다.]"
            )},
            {"role": "user", "content": user_question.question}
        ]
    
        request_data = {
            "messages": preset_text,
            "topP": 0.8,
            "topK": 0,
            "maxTokens": 256,
            "temperature": 0.5,
            "repeatPenalty": 5.0,
            "stopBefore": [],
            "includeAiFilters": True,
            "seed": randint(0,10000)
        }

        while True:
            # Clova API 실행
            response_data = completion_executor.execute(request_data)
            # API 응답 확인 및 처리
            if not response_data:
                raise HTTPException(status_code=500, detail="Clova API returned an empty response.")

            book_title, book_description = extract_book_info(response_data)
            print(f"Book Title: {book_title}")
            print(f"Book Description: {book_description}")

            # 클로바2 호출 (책 실제 확인) 딕셔너리 
            book_details = fetch_book_details_async(book_title)
            print(book_details)
            if book_title in book_details['title']:
                break
            if book_details == -1: # 책 존재 안함
                request_data["seed"]+=10
                continue
            else:
                break
            
        clovaResponse = ClovaResponse(bookimage=book_details['image'], bookTitle=book_details['title'], description=book_details['description'])
        return clovaResponse
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Clova API: {e}")


# response_data에서 책 제목과 설명 추출
def extract_book_info(response_data):
    book_title = None
    book_description = None
    result_found = False  # 'event:result'가 발견되었는지 추적

    for index, item in enumerate(response_data):
        # 'event:result'가 포함된 항목을 찾음
        if "event:result" in item:
            result_found = True  # 'event:result' 발견
            continue  # 다음 항목으로 이동

        # 'event:result' 바로 다음 항목에서 'data:' 처리
        if result_found and "data:" in item:
            try:
                json_data = item.split('data:', 1)[1].strip()
                result_data = json.loads(json_data)  
                content = result_data["message"]["content"]
                
                # 책 제목과 설명 분리
                if content.startswith("[") and "]" in content:
                    book_title = content.split("]", 1)[0][1:].strip()  # 대괄호 내부 텍스트
                    book_description = content.split("]", 1)[1].strip()  # 대괄호 이후 텍스트
                break  
            except (json.JSONDecodeError, IndexError, KeyError) as e:
                print(f"Error parsing response data: {e}")
                print(f"Problematic item: {item}")

    return book_title, book_description

# Clova API2 호출 함수
def fetch_book_details_async(book_title: str):
    class SkillSetFinalAnswerExecutor:
        def __init__(self, api_url, api_key, request_id):
            self._api_url = api_url
            self._api_key = api_key
            self._request_id = request_id

        def execute(self, skill_set_cot_request):
            headers = {
                'Authorization': self._api_key,
                'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'text/event-stream',
            }
            
            try:
                with requests.post(self._api_url, headers=headers, json=skill_set_cot_request, stream=True) as response:
                    response.raise_for_status()
                    response_data=[]
                    for line in response.iter_lines():
                        if line:
                            response_data.append(line.decode("utf-8"))
                            # print(line.decode("utf-8"))
                    return response_data
                            
            except requests.RequestException as e:
                raise HTTPException(status_code=500, detail=f"Error during Clova API call: {str(e)}")
    
    final_answer_executor = SkillSetFinalAnswerExecutor(
        api_url=f'{CLOVA_API2_URL}',
        api_key=f"Bearer {CLOVA_API_KEY}",
        request_id=CLOVA_REQUEST_ID2
    )
    request_data = {
        "query": "책",
        "tokenStream": False,
        "requestOverride": {
            "baseOperation": {
                "header": {
                    "Authorization": f"Bearer {CLOVA_API_KEY}"
                },
                "query": {
                    "appid": "appid-12345678"
                },
                "requestBody": {
                    "taskId": "book-search-task-0001"
                }
            },
            "operations": [  
                {
                    "operationId": "bookSearch",
                    "header": {
                        "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
                        "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET"),
                    },
                    "query": {
                        "sort": "sim",
                        "query": book_title,
                        "start": 1,
                        "display": 1,
                    },
                    "requestBody": None,
                }
            ]
        }
    }

    try:
        response_data = final_answer_executor.execute(request_data)
        if not response_data:
            raise HTTPException(status_code=500, detail="Clova API returned an empty response.")
        book_details = extract_book_details(response_data)
        return book_details
    except Exception as e:
        print(f"Error fetching book details: {e}")


# response_data에서 각종 책 정보 추출출
def extract_book_details(response_data):
    event_found = False # 'event:final_answer'가 발견되었느지 추적

    for index, item in enumerate(response_data):
        if "event:final_answer" in item:
            event_found = True
            continue

        if event_found and "data:" in item:
            try:
                json_data = item.split('data:', 1)[1].strip()
                result_data = json.loads(json_data)

                if "apiResult" in result_data:
                        response_body = json.loads(result_data["apiResult"][0]["responseBody"])
                        items = response_body.get("items", [])

                        if not items:
                                return -1
                        for item in items:
                            book_detail = {
                                "title": item.get("title", "N/A"),
                                "author": item.get("author", "N/A"),
                                "publisher": item.get("publisher", "N/A"),
                                "pubdate": item.get("pubdate", "N/A"),
                                "isbn": item.get("isbn", "N/A"),
                                "description": item.get("description", "N/A"),
                                "image": item.get("image", "N/A"),
                            }
                            return book_detail 
            except (json.JSONDecodeError, IndexError, KeyError) as e:
                print(f"Error parsing response data: {e}")
                print(f"Problematic item: {item}")
    return 0



# 캘린더 데이터 저장 경로
CALENDAR_DIR = "/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/calendar"
CALENDAR_FILE = os.path.join(CALENDAR_DIR, "calendar.json")

# 폴더 없으면 생성
os.makedirs(CALENDAR_DIR, exist_ok=True)

@router.post("/api/save_books")
async def save_books(calendarResponse: CalendarResponse):
    try:
        # datetime.datetime.strptime(calendarResponse.date, "%Y-%m-%d")
        # datetime.datetime.strptime(calendarResponse.time, "%H:%M")

        # 기존 데이터 불러오기 (파일이 없으면 빈 리스트 사용)
        if os.path.exists(CALENDAR_FILE):
            with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
                try:
                    calendar_data = json.load(f)
                except json.JSONDecodeError:
                    calendar_data = []
        else:
            calendar_data = []

        # 새 데이터 추가
        new_entry = calendarResponse.dict()
        calendar_data.append(new_entry)

        # JSON 파일에 저장
        with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
            json.dump(calendar_data, f, ensure_ascii=False, indent=4)

        return {
            "statusCode": 200,
            "message": "Book data saved successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date or time format: {e}")
    
@router.get("/api/calendar", response_model=List[CalendarResponse])
async def get_calendar():
    try:
        if os.path.exists(CALENDAR_FILE):
            with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
                try:
                    calendar_data = json.load(f)
                except json.JSONDecodeError:
                    raise HTTPException(status_code=500, detail="Error reading calendar file")
        else:
            calendar_data = []

        return calendar_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching calendar data: {e}")






# 뱃지 이미지 저장 폴더
BADGE_DIR = "/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/badge"

# # 폴더 없으면 생성
# os.makedirs(BADGE_DIR, exist_ok=True)

@router.post("/api/badge_create")
async def create_badge(request: BadgeRequest):
    try:
        # filenames = generate_badge(request.bookTitle, request.badgeImages) # 임시 모델 연결 코드
        return {
            "statusCode": 200,
            "message": "Badge image generated successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating badge: {e}")

# 모든 뱃지 이미지를 Base64로 변환하여 반환 (GET)
@router.get("/api/badge", response_model=List[Dict[str, str]])
async def get_all_badge_images():
    try:
        badge_images = []
        
        for file in Path(BADGE_DIR).iterdir():
            if file.is_file():
                with open(file, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                    
                badge_images.append({
                    "filename": file.name,
                    "base64": f"data:image/png;base64,{base64_image}" 
                })

        return badge_images
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching badge images: {e}")
