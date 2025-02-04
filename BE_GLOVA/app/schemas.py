from pydantic import BaseModel
from typing import List

class UserQuestion(BaseModel):
    # name: str
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
    badgeImage: str

class BadgeResponse(BaseModel):
    createdAt: str #"2025-01-27T14:00:00Z", // IISO 8601 형식    
    badgeImage: str
    bookTitle: str