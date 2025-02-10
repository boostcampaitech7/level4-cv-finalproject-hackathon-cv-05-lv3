from app.models.createBadge import create_badge
from app.models.createVoice import clova_voice
router = APIRouter()

@router.post("/api/badge")
async def create_badge(
    request: Dict[str, str],  # 북id, 대사? 성별 
    mysql_db: Session = Depends(get_mysql_db),
    user_id: str = Depends(get_user_id)  # ✅ JWT 토큰에서 `user_id` 가져오기
) -> Dict:
    """
    뱃지랑 보이스를 만들어서 리턴!
    책 표지로 뱃지 이미지 만들어서 받고
    스피크로 보이스 만들어서 받고 ㅒ(스피크는 오브젝트 테이블?) url받아서
    이미지랑 url이랑 시간 만들고, 북id랑 유저 id넣어서 뱃지 테이블 생성
    북 이미지랑 mp3 리턴? 그냥 테이블 쨰로 리턴 
    """
    try:
        book_detail = get_book(mysql_db, book_id)
        
        png_data = create_badge(book_detail.image)
        mp3_data = clova_voice(speak=speak, )
        
        # 질문을 기반으로 도서 추천 처리
        response = book_question(
            question=request.question,
            age=request.age,
            gender=request.gender
        )
        if not response:
            raise HTTPException(status_code=500, detail="추천 결과를 가져올 수 없습니다.")

        return {"status": "success", "data": response}  # ✅ JSON 형식으로 응답
    except Exception as e:
        logging.error(f"서버 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

  