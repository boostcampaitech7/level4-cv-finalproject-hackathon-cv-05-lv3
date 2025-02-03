import os
import requests
import json
import argparse
from dotenv import load_dotenv
import uuid
import datetime
import pytz

# .env 파일에서 환경 변수 로드
load_dotenv()
# 현재 UTC 시간 가져오기
utc_now = datetime.datetime.utcnow()
# 한국 시간(KST, UTC+9)으로 변환
kst = pytz.timezone('Asia/Seoul')
kst_now = utc_now.astimezone(kst)
# 원하는 형식으로 변환
timestamp = kst_now.strftime("%Y%m%d%H%M%S")

# UUID 생성
TUNING_REQUEST_ID = f"{timestamp}-{uuid.uuid4()}"
CLOVA_API_KEY = os.getenv('CLOVA_Authorization')
BUCKET_NAME = os.getenv('BUCKET_NAME')
DATASET_FILE_PATH = os.getenv('DATASET_FILE_PATH')
ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
SECRET_KEY = os.getenv('SECRET_KEY')

# CLI 인자 파싱
parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True, help="Task name")
parser.add_argument("--trainEpochs", required=True, help="Number of training epochs")
parser.add_argument("--learningRate", required=True, help="Learning rate")
args = parser.parse_args()

class CreateTaskExecutor:
    def __init__(self, host, uri, api_key):
        self._host = host
        self._uri = uri
        self._api_key = api_key

    def _send_request(self, create_request):

        headers = {
            'Authorization': self._api_key,
            'Content-Type': 'application/json',
            'X-NCP-CLOVASTUDIO-REQUEST-ID': f'{TUNING_REQUEST_ID}'
        }
        result = requests.post(self._host + self._uri, json=create_request, headers=headers).json()
        return result

    def execute(self, create_request):
        res = self._send_request(create_request)
        if 'status' in res and res['status']['code'] == '20000':
            return res['result']
        else:
            return res


if __name__ == '__main__':
    completion_executor = CreateTaskExecutor(
        host='https://clovastudio.stream.ntruss.com',
        uri='/tuning/v2/tasks',
        api_key=f'Bearer {CLOVA_API_KEY}',
    )

    request_data = {
        'name': args.name,
        'model': 'HCX-003',
        'tuningType': 'PEFT',
        'taskType': 'GENERATION',
        'trainEpochs': args.trainEpochs,
        'learningRate': args.learningRate,
        'trainingDatasetBucket': f'{BUCKET_NAME}',
        'trainingDatasetFilePath': f'{DATASET_FILE_PATH}',
        'trainingDatasetAccessKey': f'{ACCESS_KEY_ID}',
        'trainingDatasetSecretKey': f'{SECRET_KEY}'
    }
    response_text = completion_executor.execute(request_data)
    
    # log 폴더 확인 및 생성
    log_dir = "AI/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # JSON 데이터 생성
    log_data = {
        "request_data": request_data,
        "response_text": response_text
    }
    
    # 파일명 설정
    log_filename = f"{TUNING_REQUEST_ID}-{DATASET_FILE_PATH.replace('/', '_')}.json"
    log_filepath = os.path.join(log_dir, log_filename)
    
    # JSON 파일 저장
    with open(log_filepath, 'w', encoding='utf-8') as log_file:
        json.dump(log_data, log_file, ensure_ascii=False, indent=4)
    
    print(request_data)
    print(response_text)
