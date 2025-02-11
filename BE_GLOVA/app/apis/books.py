import os
from fastapi import Request, HTTPException, APIRouter, Depends
import traceback
from datetime import datetime
import secrets
from dotenv import load_dotenv
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database.connections import get_mysql_db, get_postgresql_db
from database.crud import (
    read_user, create_book,create_session, create_recommended_book, create_user_question, create_clova_answer
)
from schemas import (
    SaveBookRequest, BookSchema, SessionSchema, RecommendedBookSchema, 
    UserQuestionSchema, ClovaAnswerSchema
)

router = APIRouter()

NAVER_LOGIN_CLIENT_SECRET = os.getenv('NAVER_LOGIN_CLIENT_SECRET')
ALGORITHM = "HS256"

load_dotenv()

def get_user_id(request: Request, db: Session = Depends(get_mysql_db)) -> str:
    """
    - 쿠키에서 JWT access_token을 가져와 디코딩하여 user_id를 추출
    - 추출한 user_id가 DB에 존재하는지 검증 후 반환
    """
    # ✅ 1. 쿠키에서 access_token 가져오기
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")  # ❌ 토큰 없음

    try:
        # ✅ 2. JWT 토큰 디코딩하여 user_id 추출
        payload = jwt.decode(access_token, NAVER_LOGIN_CLIENT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")  # ❌ 토큰에서 user_id 없음

        # ✅ 3. DB에서 user_id 확인
        user = read_user(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User does not exist")  # ❌ 유저 없음

        return user_id  # ✅ 유효한 user_id 반환

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")  # ❌ JWT 인증 실패

def generate_session_id():
    """ 랜덤한 세션 ID 생성 (32자리) """
    return secrets.token_hex(16)

def parse_datetime(date_str: str, time_str: str) -> datetime:
    """ ✅ 클라이언트에서 받은 날짜와 시간을 조합하여 datetime 객체로 변환 """
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

@router.post("/api/save_books")
async def save_books(
    request: SaveBookRequest,  
    postgresql_db: Session = Depends(get_postgresql_db),
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)
):
    try:
        print("🔹 받은 데이터:", request.dict())
        print("🔹 User ID:", user_id)
        print(f"📅 서버 현재 시간: {datetime.now().isoformat()}")

        # ✅ 1️⃣ 데이터 파싱
        timestamp = parse_datetime(request.date, request.time)
        print(f"timestamp {timestamp}")
        data = request.data

        pubdate_str = data["book_info"].get("pubdate", None)

        if pubdate_str:
            try:
                if "-" in pubdate_str:  # ✅ YYYY-MM-DD 형식
                    pubdate = datetime.strptime(pubdate_str, "%Y-%m-%d")
                else:  # ✅ YYYYMMDD 형식
                    pubdate = datetime.strptime(pubdate_str, "%Y%m%d")
            except ValueError:
                print(f"❌ [오류] 잘못된 날짜 형식: {pubdate_str}")
                pubdate = None
        else:
            pubdate = None

        # ✅ 2️⃣ 책 데이터 저장
        book_data = BookSchema(
            title=data["book_info"].get("title", "제목 없음"),
            author=data["book_info"].get("author", None),
            publisher=data["book_info"].get("publisher", None),
            pubdate=pubdate,
            isbn=data["book_info"].get("isbn", None),
            description=data["book_info"].get("description", None),
            image=data["book_info"].get("image", None)
        )

        book_answer = create_book(mysql_db, book_data)

        print("📌 book_answer:", book_answer)
        print("📌 book_answer.book_id:", getattr(book_answer, 'book_id', None))

        if not book_answer or not getattr(book_answer, 'book_id', None):
            raise ValueError("📌 book_id가 None입니다! MySQL에 책이 정상적으로 저장되지 않았습니다.")
        
        # ✅ 4️⃣ 세션 생성
        session_id = generate_session_id()
        # 1️⃣ 세션을 먼저 생성 (question_id & answer_id는 나중에 설정)
        session_data = SessionSchema(
            session_id=session_id,
            question_id=0,
            answer_id=0
        )
        session_response = create_session(db=mysql_db, session_data=session_data)
        mysql_db.flush()
        print(f"📌 생성된 session_id: {session_response.session_id}")

        print("📌 question_text:", data["question_text"])
        print("📌 answer_text:", data["answer_text"])

        # 2️⃣ 질문과 답변을 PostgreSQL에 저장
        question_data = UserQuestionSchema(
            user_id=user_id,
            session_id=session_id,
            question_text=data["question_text"],
            created_at=timestamp
        )
        question_response = create_user_question(db=postgresql_db, question_data=question_data)

        answer_data = ClovaAnswerSchema(
            user_id=user_id,
            session_id=session_id,
            answer_text=data["answer_text"],
            created_at=timestamp
        )
        answer_response = create_clova_answer(db=postgresql_db, answer_data=answer_data)

        # 3️⃣ question_id & answer_id를 업데이트
        session_response.question_id = question_response.question_id
        session_response.answer_id = answer_response.answer_id
        mysql_db.commit()  # ✅ 커밋 필수

        recommended_book_data = RecommendedBookSchema(
            user_id=user_id,
            book_id=book_answer.book_id,
            session_id=session_id,
            recommended_at=timestamp,
            finished_at=None
        )
        recommended_book_response = create_recommended_book(mysql_db, recommended_book_data)
        mysql_db.commit()  # ✅ 트랜잭션 커밋

        return {"status": "success", "message": "Book data saved successfully"}

    except Exception as e:
        print("❌ [오류 발생]:", traceback.format_exc())  # ✅ 전체 스택 트레이스를 출력!
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@router.post("/api/recommand_books")
async def recommand_books():
    return {"message": "추천 도서 API"}