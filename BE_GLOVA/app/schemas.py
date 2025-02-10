from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Any
from typing import Optional

class UserQuestion(BaseModel):
    gender: str
    age: int
    question: str

class ClovaResponse(BaseModel):
    question: str
    bookimage: str
    bookTitle: str
    description: str

class CalendarResponse(BaseModel):
    date: str  # YYYY-MM-DD format
    time: str  # HH:mm format
    bookimage: str
    bookTitle: str
    question: str

class BadgeRequest(BaseModel):
    bookTitle: str
    bookImage: str
    speak: str

class BadgeResponse(BaseModel):
    createdAt: str #"2025-01-27T14:00:00Z", // IISO 8601 형식    
    badgeImage: str
    bookTitle: str

class VoiceRequest(BaseModel):
    bookTitle: str
    gender: str

# class VoiceResponse(BaseModel):
#     speak: str
#     mp3: audio/mpeg

# Users 테이블 Pydantic Schema
class UserSchema(BaseModel):
    user_id: str
    birth_year: str
    name: str
    gender: str
    phone_number: str | None
    email: str | None

    class Config:
        from_attributes = True  # ORM 변환 허용

# Token 테이블 Pydantic Schema
class TokenSchema(BaseModel):
    user_id: str
    refresh_token: str

    class Config:
        from_attributes = True  # ORM 변환 허용

# Books 테이블 Pydantic Schema
class BookSchema(BaseModel):
    book_id: int
    title: str
    author: str
    publisher: str | None
    pubdate: datetime | None
    isbn: str
    description: str
    image: str

    class Config:
        from_attributes = True

# Session 테이블 Pydantic Schema
class SessionSchema(BaseModel):
    session_id: str
    question_id: int
    answer_id: int

    class Config:
        from_attributes = True

# RecommendedBook 테이블 Pydantic Schema
class RecommendedBookSchema(BaseModel):
    recommendation_id: Optional[int] = None
    book_id: int
    user_id: str
    session_id: str
    recommended_at: datetime
    finished_at: datetime

    class Config:
        from_attributes = True

# Badge 테이블 Pydantic Schema
class BadgeSchema(BaseModel):
    badge_id: Optional[int] = None
    user_id: str
    book_id: int
    badge_image: str
    badge_audio_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Reviews 테이블 Pydantic Schema
class ReviewSchema(BaseModel):
    review_id: int
    user_id: str
    book_id: int
    review_text: str
    created_at: datetime

    class Config:
        from_attributes = True

# UserQuestions 테이블 Pydantic Schema
class UserQuestionSchema(BaseModel):
    question_id: int
    user_id: str
    session_id: str
    question_text: Any
    created_at: datetime

    class Config:
        from_attributes = True

# ClovaAnswers Pydantic Schema
class ClovaAnswerSchema(BaseModel):
    answer_id: int
    user_id: str
    session_id: str
    answer_text: Any
    created_at: datetime

    class Config:
        from_attributes = True
