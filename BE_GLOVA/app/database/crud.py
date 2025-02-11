from fastapi import HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .models import (
    User, Token, Book, Session as SessionTable,
    RecommendedBook, Badge, Review, UserQuestionORMModel, ClovaAnswer
)
from schemas import (
    UserSchema, TokenSchema, BookSchema, RecommendedBookSchema, UserQuestionSchema, ClovaAnswerSchema, SessionSchema
)

# MySQL CRUD - Users 테이블
def get_users(db: Session):
    return db.execute(select(User)).scalars().all()

def get_user(db: Session, user_id):
    # 유저 id가 존재하는지 조회
    return db.execute(select(User).where(User.user_id==user_id)).scalars().all()

def get_user_by_login(db: Session, user_id, user_pw):
    # 유저 id/pw 존재하는지 조회
    return db.execute(select(User).where(
        (User.user_id == user_id) |
        (User.user_pw == user_pw)
        )).scalars().all()


def create_user(db: Session, user_data: UserSchema):
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# user_id로 Users 테이블에서 조회
def read_user(db: Session, user_id: str):
    return db.execute(select(User).where(User.user_id == user_id)).scalar_one_or_none()  # user_id가 있으면 객체 반환, 없으면 None 반환.

# MySQL CRUD - Tokens 테이블
def get_tokens(db: Session):
    return db.execute(select(Token)).scalars().all()

def create_token(db: Session, token_data: TokenSchema):
    new_token = Token(**token_data.dict())
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token

# Tokens 테이블에서 특정 user_id가 있는지 조회
def read_token(db: Session, user_id: str):
    return db.execute(select(Token).where(Token.user_id == user_id)).scalar_one_or_none()

# MySQL CRUD - Books 테이블
def get_books(db: Session):
    return db.execute(select(Book)).scalars().all()

def get_book_by_id(db: Session, book_id: int):
    """📌 books 테이블에서 특정 book_id의 도서 조회"""
    query = select(Book).where(Book.book_id == book_id)
    return db.execute(query).scalar_one_or_none()

def get_book_with_title(db: Session, title: str):
    return db.execute(select(Book).where(Book.title==title)).scalars().first()

def create_book(db: Session, book_data: BookSchema):
    """ 책 정보를 저장하되, 같은 제목 또는 ISBN이 존재하면 기존 book_id 반환 """
    existing_book = db.execute(
        select(Book).where(
            (Book.title == book_data.title) | 
            (Book.isbn == book_data.isbn)
        )
    ).scalar_one_or_none()

    if existing_book:
        print(f"기존 도서 존재: {existing_book.book_id}")
        return existing_book  # 기존 도서 반환

    # 새 도서 저장
    new_book = Book(**book_data.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# MySQL CRUD - Sessions 테이블
def get_sessions(db: Session):
    return db.execute(select(SessionTable)).scalars().all()

def create_session(db: Session, session_data: SessionSchema):
    new_session = SessionTable(
        session_id=session_data.session_id,
        question_id=0,  # ✅ 생성 시 None (추후 업데이트)
        answer_id=0
    )
    db.add(new_session)  # ✅ 커밋은 나중에 진행 (트랜잭션 최적화)
    return new_session

def update_session(db: Session, session: SessionTable, question_id: int, answer_id: int):
    """ ✅ 기존 세션의 question_id & answer_id 업데이트 후 한 번만 커밋 """
    session.question_id = question_id
    session.answer_id = answer_id
    db.commit()

# MySQL CRUD - RecommendedBooks 테이블
def get_recommended_books(db: Session):
    return db.execute(select(RecommendedBook)).scalars().all()

def get_recommended_books_by_user(db: Session, user_id: str):
    query = (
        select(RecommendedBook)
        .where(RecommendedBook.user_id == user_id)
    )
    books = db.execute(query).scalars().all()

    # ✅ 객체를 JSON으로 변환
    return [
        {
            "recommendation_id": book.recommendation_id,
            "book_id": book.book_id,
            "session_id": book.session_id,
            "recommended_at": book.recommended_at,
        }
        for book in books
    ]

def update_recommended_books_finished_at(db: Session, user_id: str, recommendation_id: int):
    """
    ✅ 사용자의 추천 도서에 대해 'finished_at'을 현재 시간으로 업데이트하는 함수
    """
    # ✅ 1️⃣ 현재 시간 설정
    utc_now = datetime.utcnow()

    # ✅ 2️⃣ UTC → 한국 시간(KST) 변환
    kst_now = utc_now + timedelta(hours=9)

    # ✅ 2️⃣ 업데이트 실행
    query = (
        update(RecommendedBook)
        .where(
            RecommendedBook.recommendation_id == recommendation_id,
            RecommendedBook.user_id == user_id
        )
        .values(finished_at=kst_now)
    )

    result = db.execute(query)

    # ✅ 3️⃣ 업데이트된 행이 없으면 에러 발생
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="해당 recommendation_id가 존재하지 않거나 수정 권한이 없습니다.")

    db.commit()
    return kst_now

def get_recommended_books_by_user_and_session(db: Session, user_id: str, session_id: str):
    query = (
        select(RecommendedBook)
        .where(
            RecommendedBook.session_id == session_id,
            RecommendedBook.user_id == user_id
        )
    )
    return db.execute(query).scalars().all()

def create_recommended_book(db: Session, book_data: RecommendedBookSchema):
    new_book = RecommendedBook(**book_data.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# MySQL CRUD - Badges 테이블
def get_badges(db: Session):
    return db.execute(select(Badge)).scalars().all()
    # return db.query(Badge).all()

def get_user_badges(db: Session, user_id):
    # 한 유저의 모든 뱃지 조회
    return db.execute(select(Badge).where(Badge.user_id==user_id)).scalars().all()

def get_user_badge(db: Session, user_id, book_id):
    # 한 유저의 한 책에 대한 뱃지 조회
    return db.execute(select(Badge).where(Badge.user_id==user_id, Badge.book_id==book_id)).scalars().all()

def create_badge(db: Session, badge_data):
    new_badge = Badge(**badge_data)
    db.add(new_badge)
    db.commit()
    db.refresh(new_badge)
    return new_badge

# MySQL CRUD - Reviews 테이블
def get_reviews(db: Session):
    return db.execute(select(Review)).scalars().all()

def get_book_reviews(db: Session, book_id):
    # 해당 책에 대한 리뷰 전체
    return db.execute(select(Review).where(Review.book_id == book_id)).scalars().all()

def create_review(db: Session, review_data):
    new_review = Review(**review_data)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# PostgreSQL CRUD - UserQuestions 테이블
def get_user_questions(db: Session):
    return db.execute(select(UserQuestionORMModel)).scalars().all()

def get_question_by_session(db: Session, session_id: str):
    """📌 user_questions 테이블에서 특정 session_id의 질문 조회"""
    query = select(UserQuestionORMModel).where(UserQuestionORMModel.session_id == session_id)
    return db.execute(query).scalar_one_or_none()

def create_user_question(db: Session, question_data: UserQuestionSchema):
    new_question = UserQuestionORMModel(**question_data.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

def get_user1_questions(db: Session, user_id: str):
    return db.execute(select(UserQuestionORMModel).where(UserQuestionORMModel.user_id == user_id)).scalars().all()

def get_answer_by_session(db: Session, session_id: str):
    """📌 clova_answers 테이블에서 특정 session_id의 답변 조회"""
    query = select(ClovaAnswer).where(ClovaAnswer.session_id == session_id)
    return db.execute(query).scalar_one_or_none()

# PostgreSQL CRUD - ClovaAnswers 테이블
def get_clova_answers(db: Session):
    return db.execute(select(ClovaAnswer)).scalars().all()

def create_clova_answer(db: Session, answer_data: ClovaAnswerSchema):
    new_answer = ClovaAnswer(**answer_data.dict())
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer
