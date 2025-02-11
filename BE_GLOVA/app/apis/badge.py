from fastapi import APIRouter, Depends
from typing import Dict, Any
from sqlalchemy.orm import Session
from database.connections import get_mysql_db
from database.crud import create_badge, get_book_by_id
from schemas import BadgeSchema
from apis.save_books import get_user_id, parse_datetime
from models.createBadge import generate_badge

# from app.models.createVoice import clova_voice
router = APIRouter()

# 보이스 x 걍 뱃지만! 
@router.post("/api/badge_create")
async def create_badge(
    request: Dict[str, Any],  # book_id, speak
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)  # ✅ JWT 토큰에서 `user_id` 가져오기
) -> Dict:
    """
    뱃지랑 보이스를 만들어서 리턴!
    책 표지로 뱃지 이미지 만들어서 받고
    이미지랑 url이랑 시간 만들고, 북id랑 유저 id넣어서 뱃지 테이블 생성
    북 이미지랑 mp3 리턴? 그냥 테이블 쨰로 리턴 
    """
    try:
        # ✅ 1️⃣ 클라이언트에서 받은 date & time을 이용해 timestamp 생성
        timestamp = parse_datetime(request["date"], request["time"])

        user_text = request["speak"]
        book_detail = get_book_by_id(mysql_db, request["bookId"])
        
        png_data, timestamp = generate_badge(book_detail.image)

        badge = BadgeSchema(
            user_id=user_id,
            book_id=request["book_id"],
            badge_image=png_data, #?
            created_at=timestamp
        )

        badge_response = await create_badge(mysql_db, badge)

        return {
            "status": "success",
            "message": "Badge saved successfully",
            "stored_data": badge_response
        }

    except Exception as e:
        raise e     
     
@router.get("/api/badge", response_model=list[BadgeSchema], tags=["MySQL"])
async def get_user_badges(
    db: Session = Depends(get_mysql_db), 
    user_id: str = Depends(get_user_id)
):
    '''
    한 유저가 갖고있는 뱃지들 조회
    '''
    return get_user_badges(db, user_id)      

  