from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, Enum, Date, ForeignKey, Text, TIMESTAMP, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .snowflake_generator import snowflake_generator

# MySQL용 모델 베이스
MySQLBase = declarative_base()
# PostgreSQL 모델 베이스
PostgreSQLBase = declarative_base()

# 사용자 테이블 (users)
class User(MySQLBase):
    __tablename__ = "users"

    user_id = Column(String(64), primary_key=True)  # BASE64 고유 식별자
    birth_year = Column(String(4), nullable=False)
    name = Column(String(10), nullable=False)
    gender = Column(Enum("M", "F"), nullable=False)
    phone_number = Column(String(15))
    email = Column(String(255), unique=True)

    __table_args__ = (
        CheckConstraint("birth_year ~ '^[0-9]{4}$'", name="chk_birth_year_format"),
        CheckConstraint("phone_number ~ '^[0-9]{3}-[0-9]{4}-[0-9]{4}$'", name="chk_phone_number_format"),
        CheckConstraint("email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name="chk_email_format"),
    )

    # 관계 설정 (MySQL 내 테이블들과만 관계 설정)
    tokens = relationship("Token", back_populates="user")
    recommended_books = relationship("RecommendedBook", back_populates="user")
    badges = relationship("Badge", back_populates="user")
    reviews = relationship("Review", back_populates="user")

# 토큰 테이블 (tokens)
class Token(MySQLBase):
    __tablename__ = "tokens"

    user_id = Column(String(64), ForeignKey("users.user_id"), primary_key=True)
    refresh_token = Column(String(2048), nullable=False)

    # 관계 설정
    user = relationship("User", back_populates="tokens")

# 책 테이블 (books)
class Book(MySQLBase):
    __tablename__ = "books"

    book_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    publisher = Column(String(255))
    pubdate = Column(Date)
    isbn = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String(2048), nullable=False)

# 세션 테이블 (sessions)
class Session(MySQLBase):
    __tablename__ = "sessions"

    session_id = Column(String(36), primary_key=True, default=lambda: next(snowflake_generator))
    question_id = Column(BigInteger, nullable=False)  # FK: user_questions.question_id (PostgreSQL)
    answer_id = Column(BigInteger, nullable=False)  # FK: clova_answers.answer_id (PostgreSQL)

# 추천 도서 정보 테이블 (recommended_books)
class RecommendedBook(MySQLBase):
    __tablename__ = "recommended_books"

    recommendation_id = Column(BigInteger, primary_key=True, autoincrement=True)
    book_id = Column(BigInteger, ForeignKey("books.book_id"), nullable=False)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False)
    session_id = Column(String(255), ForeignKey("sessions.session_id"), nullable=False)
    recommended_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    finished_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # 관계 설정
    user = relationship("User", back_populates="recommended_books")

# 배지 테이블 (badges)
class Badge(MySQLBase):
    __tablename__ = "badges"

    badge_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False)
    book_id = Column(BigInteger, ForeignKey("books.book_id"), nullable=False)
    badge_image = Column(String(2048), nullable=False)
    badge_audio_url = Column(String(2048), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # 관계 설정
    user = relationship("User", back_populates="badges")

# 리뷰 테이블 (reviews)
class Review(MySQLBase):
    __tablename__ = "reviews"

    review_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False)
    book_id = Column(BigInteger, ForeignKey("books.book_id"), nullable=False)
    review_text = Column(String(2048), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    user = relationship("User", back_populates="reviews")

# 사용자 질문 테이블 (user_questions)
class UserQuestion(PostgreSQLBase):
    __tablename__ = "user_questions"

    question_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False)
    session_id = Column(String(36), ForeignKey("sessions.session_id"), nullable=False)
    question_text = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

# CLOVA 답변 테이블 (clova_answers)
class ClovaAnswer(PostgreSQLBase):
    __tablename__ = "clova_answers"

    answer_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False)
    session_id = Column(String(36), ForeignKey("sessions.session_id"), nullable=False)
    answer_text = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
