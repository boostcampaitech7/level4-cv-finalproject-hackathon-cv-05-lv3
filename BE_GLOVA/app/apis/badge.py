from fastapi import Request, APIRouter, Depends, HTTPException
from typing import Dict, Any
from sqlalchemy.orm import Session
from database.connections import get_mysql_db
from database.crud import save_badge_to_db, get_book_by_id, get_badges_by_id
from schemas import BadgeSchema
from apis.save_books import get_user_id, parse_datetime
from models.createBadge import generate_badge

# from app.models.createVoice import clova_voice
router = APIRouter()

# 보이스 x 걍 뱃지만! 
@router.post("/api/badge_create")
async def create_badge(
    request: Request,  # book_id, speak
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
        data = await request.json()  
        print("📌 Received request data:", data)

        if "date" not in data or "time" not in data or "bookId" not in data or "speak" not in data:
            raise HTTPException(status_code=400, detail="Missing required fields in request")

        timestamp = parse_datetime(data["date"], data["time"])
        book_id = data["bookId"]
        user_text = data["speak"]

        book_detail = get_book_by_id(mysql_db, book_id)
        if not book_detail:
            raise HTTPException(status_code=404, detail="Book not found")

        # ✅ 4️⃣ 뱃지 이미지 생성
        png_path = generate_badge(book_detail.image)

        badge = BadgeSchema(
            user_id=user_id,
            book_id=book_id,
            badge_image=png_path,
            created_at=timestamp
        )

        badge_response = save_badge_to_db(mysql_db, badge)

        return {
            "status": "success",
            "message": "Badge saved successfully",
        }

    except HTTPException as http_err:
        raise http_err  # FastAPI의 HTTPException을 클라이언트에 전달
    except Exception as e:
        print(f"❌ Error in create_badge: {e}")  # ✅ 에러 로그 추가
        raise HTTPException(status_code=500, detail="Internal Server Error")
     
@router.get("/api/badge", response_model=list[BadgeSchema], tags=["MySQL"])
async def get_user_badges(
    db: Session = Depends(get_mysql_db), 
    user_id: str = Depends(get_user_id)
):
    '''
    한 유저가 갖고있는 뱃지들 조회
    '''
    badges =  get_badges_by_id(db, user_id) 
    print(badges)

    return [BadgeSchema.from_orm(badge) for badge in badges]  


  