import pandas as pd
import http.client
import json
from datetime import datetime
import time

book_info = pd.read_csv('book_info4차.csv')

duplicates = book_info.duplicated(subset=['Book Title'], keep='first')
print(f"🔍 중복 검사: 총 {duplicates.sum()}건의 중복 도서 발견")

book_info = book_info[~duplicates]
print(f"🧹 중복 제거: {duplicates.sum()}건 삭제 후 {len(book_info)}건 유지")

book_titles = book_info['Book Title']
data_title = book_info['Book Title'].tolist()
data_detail = book_info['Final Answer'].str.extract(
    r'설명 : ([\s\S]*?)(\n섬네일|$)'
)[0].str.strip().tolist()

class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': self._api_key,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/serviceapp/v1/tasks/pxzy11u3/completions', 
                    json.dumps(completion_request), headers)
        response = conn.getresponse()
        
        if response.status == 429:
            conn.close()
            raise Exception("API rate limit exceeded")
        
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        max_retries = 60  
        base_delay = 1 
        
        for attempt in range(max_retries):
            try:
                res = self._send_request(completion_request)
                if res['status']['code'] == '20000':
                    return res['result']['text']
                else:
                    print(f"[ERROR] API 응답 오류: {res['status']['message']}")
                    return None
                    
            except Exception as e:
                if "API rate limit exceeded" in str(e):
                    if attempt < max_retries - 1:
                        current_delay = base_delay 
                        print(f"⚠️ 재시도 {attempt+1}/{max_retries}: {current_delay}초 후 재시도")
                        time.sleep(current_delay)
                        continue
                    else:
                        print(f"⚠️ 최대 재시도 횟수({max_retries}회) 초과")
                        return None
                else:
                    print(f"[ERROR] 기타 오류: {str(e)}")
                    return None
        return None

completion_executor = CompletionExecutor(
    host="clovastudio.stream.ntruss.com",
    api_key="",
    request_id=""
)

def process_description(preset_text):
    request_data = {
        'text': preset_text,
        'start': '',
        'restart': '',
        'includeTokens': False,
        'topP': 0.8,
        'topK': 4,
        'maxTokens': 300,
        'temperature': 0.85,
        'repeatPenalty': 5.0,
        'stopBefore': ['<|endoftext|>'],
        'includeAiFilters': True,
        'includeProbs': False
    }
    return completion_executor.execute(request_data)

total_books = len(data_title)
print(f"📚 총 {total_books}권의 도서 처리 시작 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

for idx, (title, detail) in enumerate(zip(data_title, data_detail)):
    try:
        progress = (idx + 1) / total_books * 100
        print(f"\n[{idx+1}/{total_books}] {title} 처리 중 ({progress:.1f}%)...")
        
        if title in book_titles.values:
            start_time = datetime.now()
            
            response_text = process_description(detail)
            if not response_text:
                print(f"⚠️ {title} 처리 실패 - 빈 응답 수신")
                continue
                
            new_entry = f"설명 : {response_text}\n섬네일"
            book_info.loc[book_info['Book Title'] == title, 'Final Answer'] = \
                book_info['Final Answer'].str.replace(
                    r'설명 : [\s\S]*?(\n섬네일|$)',
                    new_entry, 
                    regex=True
                )
            
            duration = (datetime.now() - start_time).total_seconds()
            print(f"✅ 성공적으로 업데이트 (소요 시간: {duration:.2f}초)")
            
    except Exception as e:
        print(f"⚠️ {title} 처리 중 오류 발생: {str(e)}")
        continue

book_info.to_csv('updated_book_info4.csv', index=False, encoding='utf-8-sig')
print(f"\n🎉 모든 처리 완료! 저장된 파일: updated_book_info4.csv [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")