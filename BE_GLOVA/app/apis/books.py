from fastapi import HTTPException, APIRouter
import os
import json
from ..schemas import CalendarResponse
from typing import List

router = APIRouter() # 모든 엔드포인트를 이 router에 정의하고, main에서 한 번에 추가 


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
    
@router.get("/api/get_books", response_model=List[CalendarResponse])
async def get_books():
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

