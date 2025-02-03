import faiss
import numpy as np
import pandas as pd
import http.client
import requests
import json
import time
import time
from datetime import datetime
def log_message(message, status="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color_code = ""
    if status == "success":
        color_code = "\033[92m"  # 초록색
    elif status == "error":
        color_code = "\033[91m"  # 빨간색
    elif status == "warning":
        color_code = "\033[93m"  # 노란색
    else:
        color_code = "\033[0m"   # 기본색
    
    print(f"{color_code}[{timestamp}] {message}\033[0m")

# 1. 임베딩 전용 클래스
class EmbeddingExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id
        self._request_counter = 0

    def get_embedding(self, text):
        start_time = time.time()
        log_message(f"임베딩 생성 시작: '{text[:15]}...'", "info")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self._api_key,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', 
                    '/testapp/v1/api-tools/embedding/v2',
                    json.dumps({"text": text}),
                    headers)
        
        response = conn.getresponse()
        result = json.loads(response.read())
        conn.close()

        # 요청 간 간격 조정 (API 제한 회피)
        self._request_counter += 1
        if self._request_counter % 10 == 0:
            time.sleep(5)
        duration = time.time() - start_time
        log_message(f"임베딩 생성 완료 ({duration:.2f}s)", "success")
        return np.array(result['result']['embedding'], dtype='float32')

# 2. 채팅 완료 전용 클래스 
class ChatCompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def send_request(self, messages):
        start_time = time.time()
        log_message("채팅 응답 생성 시작", "info")
        headers = {
            'Authorization': self._api_key,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            f'{self._host}/testapp/v1/chat-completions/HCX-003',
            headers=headers,
            json={
                'messages': messages,
                'temperature': 0.9,
                'topP': 0.8,
                'maxTokens': 4096
            },
            stream=False
        )

        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))
        log_message("스트리밍 응답 수신 시작", "info")
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))
        
        duration = time.time() - start_time
        log_message(f"응답 생성 완료 ({duration:.2f}s)", "success")
        return response
# 메인 실행 로직
if __name__ == '__main__':
    total_start = time.time()
    log_message("FAISS 인덱스 로드 시작")
    # FAISS 초기화
    index = faiss.read_index("vector_store.index")
    data = pd.read_csv("final_answers2791까지완료.csv")
    final_answers = data["Final Answer"].tolist()[:2791]
    log_message("FAISS 인덱스 로드 완료", "success")
    ######################################
    input_text = """나합격 책처럼 잘되어 있고 이론도 중요한것만 짧게 되어있는 컴활 2급책 없나요?"""
    ######################################
    log_message("\n" + "="*50)
    log_message("도서 추천 프로세스 시작")
    log_message(f"사용자 입력: {input_text}")
    log_message("="*50)

    # 각 단계 시간 측정
    phase_start = time.time()
    log_message("[1/4] 사용자 질문에서 키워드 추출 시작")
    chat_api = ChatCompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='Bearer nv-7971e91321b14d33afdc8380834d1822sQZV',
        request_id='a53490fd9f0f4a1f805ff105fd5d55b8'
    )

    preset_text = [
        {
            "role": "system",
            "content": f"""**사용자 질문 분석 요청**
1. 질문: "{input_text}" 

2. 분석 지침:
   - 3계층 키워드 추출 체계 적용
   - 계층별 최소 2개~최대 5개 키워드 생성
   - 동의어 통합 및 불필요한 조사 제거

3. 계층적 분석 구조:
   [1차] 표면적 키워드:
   - 질문 표면에 명시적으로 나타난 핵심 명사
   - 예시: "요리", "레시피", "식문화"

   [2차] 맥락적 키워드: 
   - 문맥 분석을 통해 도출되는 관련 개념
   - 예시: "식단 계획", "영양 균형", "계절 음식"

   [3차] 잠재적 키워드:
   - 사용자의 숨은 의도 추정을 통한 확장 개념
   - 예시: "식습관 개선", "음식 철학", "지속가능한 식생활"

4. 출력 형식:
   • 1차: [키워드1, 키워드2, ...] 
   • 2차: [키워드A, 키워드B, ...]
   • 3차: [키워드α, 키워드β, ...]"""
        },{"role":"user","content":"{input_text}"}
    ]
    key_word= chat_api.send_request(preset_text)
    key_word=key_word.json()
    key_word_content=key_word['result']['message']['content']
    ######################################
    # 전체 프로세스 단계 표시
    log_message(f"[1/4] 완료 ({time.time()-phase_start:.2f}s)", "success")

    # 각 단계 시간 측정
    phase_start = time.time()
    log_message("[2/4] 임베딩 생성 단계 시작")
    # 1단계: 임베딩 생성
    embedding_api = EmbeddingExecutor(
        host='clovastudio.stream.ntruss.com',
        api_key='Bearer nv-7971e91321b14d33afdc8380834d1822sQZV',
        request_id='acfe9c0298b741949a9636bddad56514'
    )
    
    query_vector = embedding_api.get_embedding(key_word_content)
    query_vector = query_vector.reshape(1, -1)
    faiss.normalize_L2(query_vector)
    log_message(f"[2/4] 완료 ({time.time()-phase_start:.2f}s)", "success")
    # 2단계: FAISS 검색
    phase_start = time.time()
    log_message("[3/4] 도서 검색 단계 시작")
    distances, indices = index.search(query_vector, 10)
    recommendations = [final_answers[i] for i in indices[0]]
    print(recommendations)
    log_message(f"[3/4] 완료: {len(recommendations)}개 발견 ({time.time()-phase_start:.2f}s)", "success")

    # 3단계: 채팅 응답
    phase_start = time.time()
    log_message("[4/4] 응답 생성 단계 시작")
    # 3단계: 채팅 완료 요청
    chat_api = ChatCompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='Bearer nv-7971e91321b14d33afdc8380834d1822sQZV',
        request_id='a53490fd9f0f4a1f805ff105fd5d55b8'
    )

    preset_text = [
        {
            "role": "system",
            "content": """- 당신은 지식이 풍부한 도서 큐레이터입니다.
- 사용자의 연령과 성별에 맞게 도서를 추천해주세요. 나이 : 26세, 성별 : 남성
- 사용자의 질문과 추천 도서 목록을 기반으로 가장 적합한 책 1권으로 답변합니다.
- 답변할 때 recommendation의 우선순위를 생각하지 않고 사용자의 연령과 성별을 반드시 고려해 답변해주세요.
- 자연스러운 문장으로 추천 이유를 설명해주세요.
- 추천도서 정보만을 사용하여 답변해주세요.
- 오타가 발생하지 않게 생성하고 나서 검토를 해주세요."""
        },
        {
            "role": "user",
            "content": f"질문: {input_text}\n추천도서: {', '.join(recommendations)}"
        }
    ]

    chat_api.send_request(preset_text)
    log_message(f"[4/4] 완료 ({time.time()-phase_start:.2f}s)", "success")

    # 총 실행 시간
    total_time = time.time() - total_start
    log_message(f"\n전체 프로세스 완료 (총 {total_time:.2f}초 소요)", "success")
    log_message("="*50)
