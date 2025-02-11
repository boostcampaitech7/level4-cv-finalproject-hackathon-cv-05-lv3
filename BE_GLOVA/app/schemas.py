from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional

class UserQuestion(BaseModel):
    gender: str
    age: int
    question: str

class SaveBookRequest(BaseModel):
    date: str  # YYYY-MM-DD
    time: str  # HH:mm:ss
    data: Dict[str, Any]  # ✅ 프론트에서 오는 JSON 전체를 포함

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
    gender: str

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
    book_id: Optional[int] = None  # ✅ 새 책 추가 시 book_id 자동 생성 가능
    title: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    pubdate: Optional[datetime] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ ORM 모델 변환 허용

# Session 테이블 Pydantic Schema
class SessionSchema(BaseModel):
    session_id: str
    question_id: Optional[int]  # ✅ None 허용
    answer_id: Optional[int]  # ✅ None 허용

    class Config:
        from_attributes = True

# RecommendedBook 테이블 Pydantic Schema
class RecommendedBookSchema(BaseModel):
    recommendation_id: Optional[int] = None
    book_id: int
    user_id: str
    session_id: str
    recommended_at: datetime
    finished_at: Optional[datetime] = None  # ✅ None 가능하도록 변경

    class Config:
        from_attributes = True

# Badge 테이블 Pydantic Schema
class BadgeSchema(BaseModel):
    badge_id: Optional[int] = None
    user_id: str
    book_id: int
    badge_image: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Reviews 테이블 Pydantic Schema
class ReviewSchema(BaseModel):
    review_id: Optional[int] = None
    user_id: str
    book_id: int
    review_text: str
    created_at: datetime

    class Config:
        from_attributes = True

# UserQuestions 테이블 Pydantic Schema
class UserQuestionSchema(BaseModel):
    question_id: Optional[int] = None  # ✅ 자동 생성 가능
    user_id: str
    session_id: str
    question_text: Dict[str, Any]  # ✅ JSONB 타입 사용
    created_at: datetime

    class Config:
        from_attributes = True

# ClovaAnswers Pydantic Schema
class ClovaAnswerSchema(BaseModel):
    answer_id: Optional[int] = None  # ✅ 자동 생성 가능
    user_id: str
    session_id: str
    answer_text: Dict[str, Any]  # ✅ JSONB 타입 사용
    created_at: datetime

    class Config:
        from_attributes = True