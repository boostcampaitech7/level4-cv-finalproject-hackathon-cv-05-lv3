from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import (
    User, Token, Book, Session as SessionTable,
    RecommendedBook, Badge, Review, UserQuestionORMModel, ClovaAnswer
)

# MySQL CRUD - Users 테이블
def get_users(db: Session):
    return db.execute(select(User)).scalars().all()

def create_user(db: Session, user_data):
    new_user = User(**user_data)
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
    # return db.query(Token).all()

def create_token(db: Session, token_data):
    new_token = Token(**token_data)
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

def get_book(db: Session, book_id: str):
    # 북 1개 리턴
    return db.execute(select(Book).where(Book.book_id==book_id)).scalars().all()

def create_book(db: Session, book_data):
    new_book = Book(**book_data)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# MySQL CRUD - Sessions 테이블
def get_sessions(db: Session):
    return db.execute(select(SessionTable)).scalars().all()

def create_session(db: Session, session_data):
    new_session = SessionTable(**session_data)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

# MySQL CRUD - RecommendedBooks 테이블
def get_recommended_books(db: Session):
    return db.execute(select(RecommendedBook)).scalars().all()
    # return db.query(RecommendedBook).all()

def get_recommended_books_by_user_and_session(db: Session, user_id: str, session_id: str):
    query = (
        select(RecommendedBook)
        .where(
            RecommendedBook.session_id == session_id,
            RecommendedBook.user_id == user_id
        )
    )
    return db.execute(query).scalars().all()
def create_recommended_book(db: Session, book_data):
    new_book = RecommendedBook(**book_data)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# MySQL CRUD - Badges 테이블
def get_badges(db: Session):
    return db.execute(select(Badge)).scalars().all()
    # return db.query(Badge).all()

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

def create_user_question(db: Session, question_data):
    new_question = UserQuestionORMModel(**question_data)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

def get_user1_questions(db: Session, user_id: str):
    return db.execute(select(UserQuestionORMModel).where(UserQuestionORMModel.user_id == user_id)).scalars().all()

# PostgreSQL CRUD - ClovaAnswers 테이블
def get_clova_answers(db: Session):
    return db.execute(select(ClovaAnswer)).scalars().all()

def create_clova_answer(db: Session, answer_data):
    new_answer = ClovaAnswer(**answer_data)
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer
