from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from database.connections import get_mysql_db, get_postgresql_db
from database.crud import (
    get_users, create_user, get_tokens, create_token, get_books, get_book_with_title, create_book,
    get_sessions, create_session, get_recommended_books, create_recommended_book,
    get_badges, save_badge_to_db, get_reviews, create_review, 
    get_user_questions, create_user_question, get_clova_answers, create_clova_answer
)
from schemas import (
    UserSchema, TokenSchema, BookSchema, SessionSchema, RecommendedBookSchema, 
    BadgeSchema, ReviewSchema, UserQuestionSchema, ClovaAnswerSchema
)

router = APIRouter()

# Users API (MySQL)
@router.get("/db/users", response_model=list[UserSchema], tags=["MySQL"])
async def api_get_users(db: Session = Depends(get_mysql_db)):
    """
    Users 테이블 조회
    """
    return get_users(db)

@router.post("/db/users", response_model=UserSchema, tags=["MySQL"])
async def api_create_user(user: UserSchema, db: Session = Depends(get_mysql_db)):
    """
    Users 테이블에 새로운 사용자 추가
    """
    try:
        return create_user(db, user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User 추가 중 오류 발생: {str(e)}")

# Tokens API (MySQL)
@router.get("/db/tokens", response_model=list[TokenSchema], tags=["MySQL"])
async def api_get_tokens(db: Session = Depends(get_mysql_db)):
    """
    Tokens 테이블 조회
    """
    return get_tokens(db)

@router.post("/db/tokens", response_model=TokenSchema, tags=["MySQL"])
async def api_create_token(token: TokenSchema, db: Session = Depends(get_mysql_db)):
    """
    Tokens 테이블에 새로운 토큰 추가
    """
    try:
        return create_token(db, token.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token 추가 중 오류 발생: {str(e)}")

# Books API (MySQL)
@router.get("/db/books", response_model=list[BookSchema], tags=["MySQL"])
async def api_get_books(db: Session = Depends(get_mysql_db)):
    """
    Books 테이블 조회
    """
    return get_books(db)

@router.get("/db/books/get_book_with_title", response_model=BookSchema, tags=["MySQL"])
async def api_get_book_with_title(title: str, db: Session = Depends(get_mysql_db)):
    """
    책 제목을 이용하여 Books 테이블 조회
    """
    return get_book_with_title(db, title)


@router.post("/db/books", response_model=BookSchema, tags=["MySQL"])
async def api_create_book(book: BookSchema, db: Session = Depends(get_mysql_db)):
    """
    Books 테이블에 새로운 책 추가
    """
    try:
         return create_book(db, book.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Book 추가 중 오류 발생: {str(e)}")
    
# Sessions API (MySQL)
@router.get("/db/sessions", response_model=list[SessionSchema], tags=["MySQL"])
async def api_get_sessions(db: Session = Depends(get_mysql_db)):
    """
    Sessions 테이블 조회
    """
    return get_sessions(db)


@router.post("/db/sessions", response_model=SessionSchema, tags=["MySQL"])
async def api_create_session(session: SessionSchema, db: Session = Depends(get_mysql_db)):
    """
    Sessions 테이블에 새로운 세션 추가
    """
    try:
        return create_session(db, session.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session 추가 중 오류 발생: {str(e)}")

# RecommendedBooks API (MySQL)
@router.get("/db/recommended_books", response_model=list[RecommendedBookSchema], tags=["MySQL"])
async def api_get_recommended_books(db: Session = Depends(get_mysql_db)):
    """
    RecommendedBooks 테이블 조회
    """
    return get_recommended_books(db)

@router.post("/db/recommended_books", response_model=RecommendedBookSchema, tags=["MySQL"])
async def api_create_recommended_book(recommended_book: RecommendedBookSchema, db: Session = Depends(get_mysql_db)):
    """
    RecommendedBooks 테이블에 새로운 추천 도서 추가
    """
    try:
        return create_recommended_book(db, recommended_book.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RecommendedBook 추가 중 오류 발생: {str(e)}")

# Badges API (MySQL)
@router.get("/db/badges", response_model=list[BadgeSchema], tags=["MySQL"])
async def api_get_badges(db: Session = Depends(get_mysql_db)):
    """
    Badges 테이블 조회
    """
    return get_badges(db)

@router.post("/db/badges", response_model=BadgeSchema, tags=["MySQL"])
async def api_create_badge(badge: BadgeSchema, db: Session = Depends(get_mysql_db)):
    """
    Badges 테이블에 새로운 배지 추가
    """
    try:
        return create_badge(db, badge.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Badge 추가 중 오류 발생: {str(e)}")

# Reviews API (MySQL)
@router.get("/db/reviews", response_model=list[ReviewSchema], tags=["MySQL"])
async def api_get_reviews(db: Session = Depends(get_mysql_db)):
    """
    Reviews 테이블 조회
    """
    return get_reviews(db)

@router.post("/db/reviews", response_model=ReviewSchema, tags=["MySQL"])
async def api_create_review(review: ReviewSchema, db: Session = Depends(get_mysql_db)):
    """
    Reviews 테이블에 새로운 리뷰 추가
    """
    try:
        return create_review(db, review.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Review 추가 중 오류 발생: {str(e)}")

# UserQuestions API (PostgreSQL)
@router.get("/db/user_questions", response_model=list[UserQuestionSchema], tags=["PostgreSQL"])
async def api_get_user_questions(db: Session = Depends(get_postgresql_db)):
    """
    UserQuestions 테이블 조회  
    """
    return get_user_questions(db)

@router.post("/db/user_questions", response_model=UserQuestionSchema, tags=["PostgreSQL"])
async def api_create_user_question(question: UserQuestionSchema, db: Session = Depends(get_postgresql_db)):
    """
    UserQuestions 테이블에 새로운 질문 추가
    """
    try:
        return create_user_question(db, question.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"UserQuestion 추가 중 오류 발생: {str(e)}")

# ClovaAnswers API (PostgreSQL)
@router.get("/db/clova_answers", response_model=list[ClovaAnswerSchema], tags=["PostgreSQL"])
async def api_get_clova_answers(db: Session = Depends(get_postgresql_db)):
    """
    ClovaAnswers 테이블 조회  
    """
    return get_clova_answers(db)

@router.post("/db/clova_answers", response_model=ClovaAnswerSchema, tags=["PostgreSQL"])
async def api_create_clova_answer(answer: ClovaAnswerSchema, db: Session = Depends(get_postgresql_db)):
    """
    ClovaAnswers 테이블에 새로운 답변 추가  
    """
    try:
        return create_clova_answer(db, answer.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ClovaAnswer 추가 중 오류 발생: {str(e)}")