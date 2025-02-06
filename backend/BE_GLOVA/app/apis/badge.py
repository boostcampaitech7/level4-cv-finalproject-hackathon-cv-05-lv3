from fastapi import HTTPException, APIRouter
from fastapi.responses import FileResponse
import json
from schemas import BadgeRequest, VoiceRequest
import base64
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv
import urllib.parse
import urllib.request
# from ..model import generate_badge

router = APIRouter() # 모든 엔드포인트를 이 router에 정의하고, main에서 한 번에 추가 

load_dotenv()

# 클로바 보이스 키 설정
CLOVA_VOICE_CLIENT_ID = os.getenv('CLOVA_VOICE_CLIENT_ID')
CLOVA_VOICE_CLIENT_SECRET = os.getenv('CLOVA_VOICE_CLIENT_SECRET')

# 뱃지 이미지 저장 폴더
BADGE_DIR = Path("/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/badge")
# BADGE_DIR = Path(__file__).parent / "badge"
METADATA_FILE = Path("/data/ephemeral/home/whth/level4-cv-finalproject-hackathon-cv-05-lv3/BE_GLOVA/badge/badge_metadata.json")
# METADATA_FILE = Path(BADGE_DIR) / "badge_metadata.json"

def clova_voice(speak: str, dir_name: str):
    class VoiceExecutor:
        def __init__(self, client_id, client_secret):
            self.client_id = client_id
            self.client_secret = client_secret
        
        def execute(self, request_data, name, VOICE_DIR):
            data = urllib.parse.urlencode(request_data).encode("utf-8")
            url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
            headers = {
                "X-NCP-APIGW-API-KEY-ID" : self.client_id,
                "X-NCP-APIGW-API-KEY" : self.client_secret
            }
            request = urllib.request.Request(url, data=data, headers=headers)
            try:
                with urllib.request.urlopen(request) as response:
                    rescode = response.getcode()
                    if rescode == 200:
                        print("TTS mp3 save")
                        response_body = response.read()
                        with open(os.path.join(VOICE_DIR, name), 'wb') as f:
                            f.write(response_body)
                    else:
                        print(f"Error Code: {rescode}")
            except urllib.error.URLError as e:
                print(f"Request failed: {e.reason}")
    
    voice_execute = VoiceExecutor(
        client_id= CLOVA_VOICE_CLIENT_ID,
        client_secret= CLOVA_VOICE_CLIENT_SECRET
    )
    
    text = speak
    speaker = "dara-danna" 
    speed = "0"
    volume = "0"
    pitch = "0"
    fmt = "mp3"
    val = {
        "speaker": speaker,
        "volume": volume,
        "speed":speed,
        "pitch": pitch,
        "text":text,
        "format": fmt
    }
    try:
        # 저장 위치 : 뱃지/뱃지 이름/
        VOICE_DIR = Path(BADGE_DIR) / dir_name
        if not os.path.exists(VOICE_DIR):
            os.makedirs(VOICE_DIR)
        voice_execute.execute(val, "female.mp3", VOICE_DIR)
        val["speaker"] = "dsinu-matt"
        voice_execute.execute(val, "male.mp3", VOICE_DIR)

    except Exception as e:
        print(f"Error fetching book details: {e}")



# 뱃지 생성 + 보이스 생성(양성)
@router.post("/api/badge_create")
async def create_badge(request: BadgeRequest):
    try:
        # 저장 위치 : 뱃지/ 뱃지 이름=책제목+시간/ 
        # timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        dir_name = f"{request.bookTitle.replace(' ', '_')}"
        DIR = Path(BADGE_DIR) / dir_name

        os.mkdir(DIR)

        # filenames = generate_badge(request.bookTitle, request.badgeImages, dir_naem) # 임시 모델 연결 코드
        clova_voice(request.speak, dir_name)
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

# 책제목? 성별 -> 대사 음성 
@router.post("/api/badge/voice")
async def download_voice(request: VoiceRequest):
    try:
        # 책 제목보고 음성 찾아서
        # 성별로 하나만 가져와서
        # time = request.time.replace(':', '-')
        # time = "2025-02-05T01-13-13" 책 하나당 하나만 만들겟대여~
        dir_name = f"{request.bookTitle.replace(' ', '_')}"
        gender = f"{request.gender}.mp3"
        DIR = Path(BADGE_DIR) / dir_name / gender
        
        print(DIR)
        
        return FileResponse(DIR, media_type="audio/mpeg", filename="output.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching badge images: {e}")
