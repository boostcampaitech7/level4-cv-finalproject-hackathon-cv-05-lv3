from fastapi import Request, APIRouter, Depends, HTTPException # HTTPException - 김건우 추가
from sqlalchemy.orm import Session
from pydantic import BaseModel # 김건우 추가
from ..database.connections import get_mysql_db
from ..database.crud import get_user_badge, get_book_reviews
from .save_books import get_user_id
from typing import List, Union # 김건우 추가가

router = APIRouter()

class BookIDRequest(BaseModel):
    book_id: int  # 클라이언트에서 받을 book_id 값

# 이 책에 대한 리뷰 작성 페이지로 감. 많은 후기들이 있으면 보여짐
# 프론트가 유저 id인 리뷰 찾고싶음 찾으라고 user_id도 줬음
# 이 리뷰 쓴 사람이 이 책을 읽고 뱃지 만들엇으면 뱃지도 넣어야함 
@router.post("/api/get_reviews")  # ✅ POST 방식으로 변경
async def get_book_reviews_badges(
    request_data: BookIDRequest,  # ✅ JSON 데이터 받기
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id),
):
    try:
        book_id = request_data.book_id  # ✅ Pydantic을 사용하여 JSON 데이터 파싱

        reviews = get_book_reviews(mysql_db, book_id)

        # ✅ Debugging 로그
        print(f"📌 리뷰 리스트: {reviews}")  

        review_badge = []
        for review in reviews:
            badge = get_user_badge(mysql_db, review.user_id, book_id)
            review_badge.append([review, badge if badge else -1])  # ✅ 뱃지가 없으면 -1

        return {
            "review_badge": review_badge,
            "user_id": user_id  # ✅ 프론트에서 내가 작성한 리뷰를 맨 위에 배치하도록 활용
        }

    except Exception as e:
        print(f"🚨 오류 발생: {str(e)}")  # ✅ 오류 로그 추가
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

# 리뷰 작성은 잇고 ㅇㅇ

