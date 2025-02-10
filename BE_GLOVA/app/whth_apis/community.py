

# 이 책에 대한 리뷰 작성 페이지로 감. 많은 후기들이 있으면 보여짐
# 프론트가 유저 id인 리뷰 찾고싶음 찾으라고 user_id도 줬음

async def get_book_reviews(
    postgresql_db: Session = Depends(get_postgresql_db),
    mysql_db: Session = Depends(get_mysql_db),
    request: Dict[str, str]
    # user_id: str = Depends(get_user_id),
    # book_id: str
):
    try:
        reviews = get_book_reviews(db, book_id)
        
        return  {
            "reviews": reviews,
            "user_id": user_id
        }
    
    except Exception as e:
        raise e

# 리뷰 작성은 잇고 ㅇㅇ