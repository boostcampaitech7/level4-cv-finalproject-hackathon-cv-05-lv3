from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.connections import get_mysql_db, get_postgresql_db
from database.crud import get_recommended_books_by_user, get_book_by_id, get_question_by_session, get_answer_by_session
from apis.save_books import get_user_id

router = APIRouter()

# 이 유저가 추천받은 책들 겟 
@router.get("/api/recommended_books")
async def get_recommended_books(
    postgresql_db: Session = Depends(get_postgresql_db),
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)
):
    try:

        # ✅ user_id에 해당하는 추천 도서 조회
        recommended_books = get_recommended_books_by_user(mysql_db, user_id)

        books_with_questions_and_answers = []

        # ✅  book_id와 session_id 기반으로 books, user_questions, clova_answers 데이터 조회
        for rec in recommended_books:
            book = get_book_by_id(mysql_db, rec["book_id"])
            question = get_question_by_session(postgresql_db, rec["session_id"])
            answer = get_answer_by_session(postgresql_db, rec["session_id"])

            # ✅ 데이터를 JSON으로 변환
            books_with_questions_and_answers.append({
                "book": {
                    "title": book.title if book else "N/A",
                    "image": book.image if book else "N/A"
                },
                "session_id": rec["session_id"],
                "question": question.question_text if question else "N/A",
                "answer": answer.answer_text if answer else "N/A"
            })

        print("📌 최종 데이터:", books_with_questions_and_answers)
        
        return {
            "status": "success",
            "message": "Recommended books with questions and answers retrieved successfully",
            "response_body": books_with_questions_and_answers
        }
        
    except Exception as e:
        print(f"❌ [오류 발생]: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


# # 책 하나를 눌름     
# @router.get("/api/get_book")
# async def get_recommended_book(
#     book_id: int,
#     mysql_db: Session = Depends(get_mysql_db),
# ):
#     try:
#         recommen
#         return get_book(mysql_db, book_id)
    
#     except Exception as e:
#         raise e



