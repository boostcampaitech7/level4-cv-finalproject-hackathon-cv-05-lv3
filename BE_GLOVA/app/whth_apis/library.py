

@router.get("/api/get_books")
async def get_books(
    postgresql_db: Session = Depends(get_postgresql_db),
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)
):
    try:
        question_recommendedBook = []
        # 유저 id인 유저 퀘스션을 모두 찾아.
        user_questions = get_user1_questions(postgresql_db, user_id)

        # 세션 id를 하나하나 돌면서 유저 퀘스션 그 값과 레커멘디드 북스 (유저id세션id) 그 값을 묶어
        for question in user_questions:
            recommended_book = get_recommended_books_by_user_and_session(mysql_db, user_id, question.session_id)
            question_recommendedBook.append([question, recommended_book])
        
        # 리스트에 유저퀘스션-레커멘디드북 쌍으로 모두 리턴
        return {
            "status": "success",
            "message": " successfully",
            "response_body": question_recommendedBook
        }
        
    except Exception as e:
        raise e

# 책 하나를 눌름     
@router.get("/api/get_book")
async def get_book(
    postgresql_db: Session = Depends(get_postgresql_db),
    mysql_db: Session = Depends(get_mysql_db),
    book_id: str
):
    try:
        return get_book(mysql_db, book_id)
    
    except Exception as e:
        raise e



