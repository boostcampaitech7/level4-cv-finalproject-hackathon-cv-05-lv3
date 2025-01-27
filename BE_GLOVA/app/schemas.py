from pydantic import BaseModel
from typing import List

class UserQuestion(BaseModel):
    name: str
    sex: str
    age: int
    answer: str

class ClovaResponse(BaseModel):
    title: str
    description: str

class KeywordResponse(BaseModel):
    keywords: List[str]

class ImageResponse(BaseModel):
    image: str