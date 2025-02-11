from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session
from database.connections import get_mysql_db
from database.crud import get_user_badge, get_book_reviews
from apis.save_books import get_user_id

router = APIRouter()

# 이 책에 대한 리뷰 작성 페이지로 감. 많은 후기들이 있으면 보여짐
# 프론트가 유저 id인 리뷰 찾고싶음 찾으라고 user_id도 줬음
# 이 리뷰 쓴 사람이 이 책을 읽고 뱃지 만들엇으면 뱃지도 넣어야함 
@router.get("/api/get_reviews")
async def get_book_reviews_badges(
    request : Request,
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id),
):
    try:
        data = await request.json()
        book_id = data["bookId"]
        reviews = get_book_reviews(mysql_db, book_id)

        print(reviews.dict())
        
        review_badge = []
        for review in reviews:
            if get_user_badge(mysql_db, review.user_id, book_id):
                review_badge.append([review, get_user_badge(mysql_db, review.user_id, book_id)])
            else:
                review_badge.append([review, -1]) # 프론트야 -1이 뜨면 뱃지 없는 사람이라고 생각해줘.
            
        return  {
            "review_badge": review_badge,
            "user_id": user_id # 이걸로 내가 리뷰 썼으면 맨 위에 올려줘
        }
    
    except Exception as e:
        raise e

# 리뷰 작성은 잇고 ㅇㅇ

