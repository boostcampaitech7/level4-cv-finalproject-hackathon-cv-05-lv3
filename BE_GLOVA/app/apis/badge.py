from fastapi import HTTPException, APIRouter
import json
from schemas import BadgeRequest
import base64
from pathlib import Path
# from ..model import generate_badge

router = APIRouter() # 모든 엔드포인트를 이 router에 정의하고, main에서 한 번에 추가 

# 뱃지 이미지 저장 폴더
BADGE_DIR = Path("/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/badge")
# BADGE_DIR = Path(__file__).parent / "badge"
METADATA_FILE = Path("/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/badge/badge_metadata.json")
# METADATA_FILE = Path(BADGE_DIR) / "badge_metadata.json"

# # 폴더 없으면 생성
# os.makedirs(BADGE_DIR, exist_ok=True)

@router.post("/api/badge_create")
async def create_badge(request: BadgeRequest):
    try:
        # filenames = generate_badge(request.bookTitle, request.badgeImages) # 임시 모델 연결 코드
        return {
            "statusCode": 200,
            "message": "Badge image generated successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating badge: {e}")

# 모든 뱃지 이미지를 Base64로 변환하여 반환 (GET)
@router.get("/api/badge") #, response_model=List[Dict[str, str]]
async def get_all_badge_images():
    try:
        if not  Path(METADATA_FILE).exists():
            return {"statusCode": 200, "badges": []}
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            badge_metadata = json.load(f)
        
        badge_images = []
            
        for file in Path(BADGE_DIR).iterdir():
            if file.is_file() and file.name in badge_metadata:
                with open(file, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                        
                badge_images.append({
                    "createdAt": f"{badge_metadata[file.name]['createdAt']}Z", 
                    "badgeImage": f"data:image/png;base64,{base64_image}",
                    "bookTitle": badge_metadata[file.name]["bookTitle"]
                })
        return badge_images
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching badge images: {e}")
