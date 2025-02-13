import faiss
import numpy as np
import pandas as pd
import http.client
import requests
import json
import time
import re
from datetime import datetime
from collections import defaultdict
import sys
def deduplicate_recommendations(all_results, data):
    doc_counts = defaultdict(int)
    doc_scores = defaultdict(list)
    content_hashes = set()
    
    # 1단계: 점수 집계
    for doc_id, score in all_results:
        doc_counts[doc_id] += 1
        doc_scores[doc_id].append(score)
    
    # 2단계: 중복 내용 필터링
    unique_docs = []
    #print(data[:5])
    for doc_id in sorted(doc_counts.keys(), 
                        key=lambda x: (-doc_counts[x], min(doc_scores[x]))):
        content = data[doc_id]
        #print(content)
        content_hash = hash(content[:100])  # 첫 100자 기반 해시
        if content_hash not in content_hashes:
            content_hashes.add(content_hash)
            unique_docs.append(doc_id)
    
    return unique_docs[:1000]  # 상위 5개 반환

# 로깅 설정 (기존 코드 유지)
def log_message(message, status="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color_code = ""
    if status == "success":
        color_code = "\033[92m"
    elif status == "error":
        color_code = "\033[91m"
    elif status == "warning":
        color_code = "\033[93m"
    else:
        color_code = "\033[0m"
    print(f"{color_code}[{timestamp}] {message}\033[0m")

# 1. 계층별 키워드 파싱 클래스
class KeywordProcessor:
    def __init__(self):
        self.keyword_pattern = re.compile(r'(\d차)\s*:\s*\[([^\]]+)\]') 

    def parse_keywords(self, content):
        extracted = {}
        for level, key_str in self.keyword_pattern.findall(content):
            keywords = [
                k.strip().strip('"') 
                for k in key_str.split(',')
                if k.strip().strip('"')
            ]
            extracted[level] = keywords

        weighted_keys = []
        for idx, level in enumerate(['1차', '2차', '3차'], 1):
            weight = 4 - idx
            weighted_keys.extend([(k, weight) for k in extracted.get(level, [])])
        
        return weighted_keys

# 2. FAISS 필터링 클래스 (검색 결과 [3] 참조)
class KeywordFilter(faiss.IDSelector):
    def __init__(self, valid_ids):
        self.valid_ids = set(valid_ids)
    
    def is_member(self, id):
        return id in self.valid_ids

# 임베딩 & 채팅 클래스 (기존 코드 유지)
class EmbeddingExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id
        self._request_counter = 0

    def get_embedding(self, text):
        max_retries = 1000
        base_delay = 1  # 초기 지연 시간(초)
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                log_message(f"임베딩 생성 시도 {attempt+1}/{max_retries}: '{text}'", "info")
                
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': self._api_key,
                    'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
                }

                conn = http.client.HTTPSConnection(self._host, timeout=10)
                conn.request('POST', 
                            '/serviceapp/v1/api-tools/embedding/v2',
                            json.dumps({"text": text}),
                            headers)
                
                response = conn.getresponse()
                if response.status != 200:
                    raise http.client.HTTPException(f"HTTP 오류: {response.status} {response.reason}")
                
                result = json.loads(response.read())
                conn.close()

                # 요청 간 간격 조정
                self._request_counter += 1
                if self._request_counter % 10 == 0:
                    time.sleep(5)
                    
                duration = time.time() - start_time
                log_message(f"임베딩 생성 완료 ({duration:.2f}s)", "success")
                return np.array(result['result']['embedding'], dtype='float32')

            except (http.client.HTTPException, ConnectionError, TimeoutError) as e:
                log_message(f"임베딩 요청 실패: {str(e)}", "error")
                if attempt == max_retries - 1:
                    raise
                delay = 1  # 지수 백오프
                time.sleep(delay)


class ChatCompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def send_request(self, messages):
        max_retries = 1000
        base_delay = 1  # 초기 지연 시간(초)
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                log_message(f"채팅 요청 시도 {attempt+1}/{max_retries}", "info")
                
                headers = {
                    'Authorization': self._api_key,
                    'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
                    'Content-Type': 'application/json'
                }

                response = requests.post(
                    f'{self._host}/serviceapp/v1/chat-completions/HCX-003',
                    headers=headers,
                    json={
                        'messages': messages,
                        'temperature': 0.9,
                        'topP': 0.8,
                        'maxTokens': 4096,
                    },
                    timeout=10,
                    stream=False
                )
                response.raise_for_status() 
                
                log_message("스트리밍 응답 수신 시작", "info")
                for line in response.iter_lines():
                    if line:
                        print(line.decode('utf-8'))
                
                duration = time.time() - start_time
                log_message(f"응답 생성 완료 ({duration:.2f}s)", "success")
                return response
            except (requests.exceptions.RequestException, TimeoutError) as e:
                if e.response.status_code==400:
                    log_message("400 오류: 추천 리스트 크기 조정 시도", "warning")
                    return response
                log_message(f"채팅 요청 실패: {str(e)}", "error")
                if attempt == max_retries - 1:
                    raise
                delay = 1 
                time.sleep(delay)

if __name__ == '__main__':
    total_start = time.time()
    log_message("FAISS 인덱스 로드 시작")
    index = faiss.read_index("vector_store_최종_plz_no_error.index")
    index_title = faiss.read_index("vector_store_최종_only_title.index")
    data = pd.read_csv("sorted.csv")
    descriptions = data["Description"].tolist()
    titles = data["Book Title"].tolist()
    combined=[]
    for i in range(len(titles)):
        combined_entry = f"{{{titles[i]}}},{{{descriptions[i]}}}" 
        combined.append(combined_entry)

    #final_answers = list(zip(final_title, final_answer))
    final_answers = combined
    data2 = pd.read_csv("book_data_final진짜마지막임.csv")
    final_answers2 = data2["Final Answer"].tolist()
    log_message("FAISS 인덱스 로드 완료", "success")
    ######################################
    input_text = """드디어 끝났다. 행복하다"""
    ######################################
    log_message("\n" + "="*50)
    log_message("도서 추천 프로세스 시작")
    log_message(f"사용자 입력: {input_text}")
    log_message("="*50)

    # 각 단계 시간 측정
    phase_start = time.time()
    log_message("[1/4] 계층별 키워드 추출 시작")
    chat_api = ChatCompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='', #api 키를 넣어주세요
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
    processor = KeywordProcessor()
    weighted_keywords = processor.parse_keywords(key_word_content)
    repeat=0
    while(len(weighted_keywords)<1):
        repeat=repeat+1
        key_word= chat_api.send_request(preset_text)
        key_word=key_word.json()
        key_word_content=key_word['result']['message']['content']
        processor = KeywordProcessor()
        weighted_keywords = processor.parse_keywords(key_word_content)
        if (len(weighted_keywords)>1):
            break
        if repeat>5:
            print("프롬프트 이상이 검출 되었습니다.") 
            sys.exit(1)
    only_keywords=[i for i,answer in weighted_keywords]
    embedding_api = EmbeddingExecutor(
        host='clovastudio.stream.ntruss.com',
        api_key='',#api키를 입력해주세요
        request_id='acfe9c0298b741949a9636bddad56514'
    )
    
    log_message(f"[1/4] 완료 ({time.time()-phase_start:.2f}s)", "success")
    phase_start = time.time()
    log_message("[2/4] 키워드별 임베딩 생성 및 faiss 탐색 단계 시작")
    
    
    all_results = []
    for keyword, weight in weighted_keywords:
        # 개별 키워드 임베딩 생성
        keyword_embedding = embedding_api.get_embedding(keyword)
        keyword_embedding = keyword_embedding.reshape(1, -1)
        faiss.normalize_L2(keyword_embedding)
        
        # 개별 키워드 검색
        distances, indices = index.search(keyword_embedding, 10)
        
        # 결과 수집 (가중치 적용)
        for idx, score in zip(indices[0], distances[0]):
            if idx != -1:
                adjusted_score = score #* weight
                all_results.append((idx, adjusted_score))
    #print(all_results,"all_result")
    #print(len(all_results))
    log_message(f"[2/4] 완료 ({time.time()-phase_start:.2f}s)", "success")
    phase_start = time.time()
    log_message("[3/4] 책추천 우선순위 설정중")
    # 중복 제거 및 최종 추천 생성
    final_docs = deduplicate_recommendations(all_results, final_answers)
    recommendations = [final_answers[doc_id] for doc_id in final_docs]
    #print(len(recommendations))
    log_message(f"[3/4] 완료 ({time.time()-phase_start:.2f}s)", "success")
    phase_start = time.time()
    log_message("[4/4] 응답 생성 단계 시작")
    # 3단계: 채팅 완료 요청
    chat_api = ChatCompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='',#api key를 입력해주세요.
        request_id='a53490fd9f0f4a1f805ff105fd5d55b8'
    )
    
    preset_text = [
        {
            "role": "system",
            "content": f"""- 당신은 지식이 풍부한 도서 큐레이터입니다.
- 사용자의 연령과 성별에 맞게 도서를 추천해주세요. 나이 : 26세, 성별 : 남성
- 사용자의 질문과 추천 도서 목록을 기반으로 가장 적합한 책 1권으로 답변합니다.
- 답변할 때 recommendation의 우선순위를 생각하지 않고 사용자의 연령과 성별을 고려해 답변해주세요.
- 자연스러운 문장으로 사용자의 질문과 연관된 추천 이유를 설명해주세요.
- 추천도서 정보만을 사용하여 답변해주세요.
- 오타가 발생하지 않게 생성하고 나서 검토를 해주세요.
- 사용자의 질문과 추천 도서 목록을 기반으로 가장 적합한 책 1권으로 사용자의 질문과 연관된 추천이유를 답변 합니다.
- 답변할 때 제시된 키워드를 생각하고, 자연스러운 문장으로 추천이유를 답변해주세요.
- 사용자가 비슷한 책을 추천해달라고 할 때 절대 사용자의 질문과 동일한 책을 추천하지 않습니다.
- 제시된 키워드 : "{only_keywords}"
- 답변형식 : {{
추천하는 책 : []
추천이유 :}} """
        },
        {
            "role": "user",
            "content": f"질문: {input_text}\n추천도서: {', '.join(recommendations)}"
        }
    ]
    #response = chat_api.send_request(preset_text)
    
    max_recommend = 1000  # 최초 추천 개수
    
    max_recommend = len(recommendations)  # 초기 추천 개수
    content = f"질문: {input_text}\n추천도서: {', '.join(recommendations[:max_recommend])}"

    while len(content.encode('utf-8')) >= 4050 and max_recommend > 1:
        max_recommend -= 1
        content = f"질문: {input_text}\n추천도서: {', '.join(recommendations[:max_recommend])}"
    
    print(max_recommend)
    
    for retry in range(30): 
    #try:
        preset_text[1]['content'] = f"질문: {input_text}\n추천도서: {', '.join(recommendations[:max_recommend])}"
        #print(preset_text)
        response = chat_api.send_request(preset_text)
        if response.status_code == 200:
            break
    #except requests.exceptions.HTTPError as e:
        #if e.response.status_code == 400:
        max_recommend = max(1, max_recommend-1)  # 1개까지 축소
        log_message(f"추천 개수 조정: {max_recommend}개로 재시도", "warning")
    
    log_message(f"[4/4] 완료 ({time.time()-phase_start:.2f}s)", "success")
    
    phase_start = time.time()
    log_message("[5/5] 응답 데이터 찾기 시작")
    response=response.json()
    content = response['result']['message']['content']
    book_match = re.search(r'추천하는 책\s*:\s*(.*?)\n', content)
    
    if book_match:
        book_title = book_match.group(1).strip()
        print(f"추천 도서: {book_title}")
    else:
        print("책 제목을 찾을 수 없습니다")
    
    book_embedding = embedding_api.get_embedding(book_title)
    book_embedding = book_embedding.reshape(1, -1)
    faiss.normalize_L2(book_embedding)
    
    # 개별 키워드 검색
    distances, indices = index_title.search(book_embedding, 1)
    log_message(f"[5/5] 완료 ({time.time()-phase_start:.2f}s)", "success")
    print(final_answers2[indices[0][0]])
    
    # 총 실행 시간
    total_time = time.time() - total_start
    log_message(f"\n전체 프로세스 완료 (총 {total_time:.2f}초 소요)", "success")
    log_message("="*50)
