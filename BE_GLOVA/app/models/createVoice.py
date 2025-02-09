from pathlib import Path
import os
from dotenv import load_dotenv
import urllib.parse
import urllib.request

# 오디오 생성 함수
# 저장 위치 같은 거 지우고 어...아닌가? url로 어케 만들지?

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

