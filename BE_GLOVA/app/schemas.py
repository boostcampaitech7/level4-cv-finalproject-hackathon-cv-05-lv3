from pydantic import BaseModel
from typing import List

class UserQuestion(BaseModel):
    name: str
    gender: str
    age: int
    answer: str

class ClovaResponse(BaseModel):
    bookimage: str
    bookTitle: str
    description: str

class KeywordResponse(BaseModel):
    keywords: List[str]

class ImageResponse(BaseModel):
    image: str