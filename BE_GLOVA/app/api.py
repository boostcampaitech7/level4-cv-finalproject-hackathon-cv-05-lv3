from fastapi import FastAPI, HTTPException, Request, APIRouter
from dotenv import load_dotenv
import requests
import os
import json
import re
from schemas import UserQuestion, ClovaResponse, KeywordResponse, ImageResponse

router = APIRouter() # 모든 엔드포인트를 이 router에 정의하고, main에서 한 번에 추가 

load_dotenv()

CLOVA_API_URL = "https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003"
CLOVA_API_KEY = os.getenv('CLOVA_Authorization')
if not CLOVA_API_KEY:
    raise ValueError("CLOVA_Authorization 환경 변수가 설정되지 않았습니다.")
CLOVA_REQUEST_ID = os.getenv('CLOVA_REQUEST_ID') # <- 임시 테스트 앱 리퀘스트 id, 실제 서비스와 연동 시 변경되므로 .env에서 변경!


@router.post("/api/question")
async def save_question(user_question: UserQuestion, request: Request):
    class CompletionExecutor:
        def __init__(self, host, api_key, request_id):
            self._host = host
            self._api_key = api_key
            self._request_id = request_id

        def execute(self, completion_request):
            headers = {
                'Authorization': self._api_key,
                'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'text/event-stream'
            }

            with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                               headers=headers, json=completion_request, stream=True) as r:
                response_data = []
                for line in r.iter_lines():
                    if line:
                        response_data.append(line.decode("utf-8"))
                return response_data

    try:
        # Clova API 설정
        completion_executor = CompletionExecutor(
            host="https://clovastudio.stream.ntruss.com",
            api_key=f"Bearer {CLOVA_API_KEY}",
            request_id=f"Bearer {CLOVA_REQUEST_ID}" 
        )
        preset_text = [
            {
                "role": "system",
                "content": f"- 당신은 지식이 풍부한 도서 큐레이터입니다.\n"
                           f"- 사용자의 나이 : {user_question.age}, 성별 : {user_question.sex}\n"
                           f"- 사용자의 질문에 대해 사용자의 나이, 성별을 분석하여 "
                           f"- 시중에 있는 책에서 관련 내용을 인용하거나 추천하는 방식으로 답변합니다.\n"
                           f"- 사용자의 질의를 분석하고 질의와 상관관계를 보이는 책 제목으로 답해줘\n"
                           f"- 1개의 답변이고, 명확하고 간결하며, 독자가 흥미를 느낄 수 있도록 작성하세요.\n"
                           f"예시:\n"
                           f"질문: 아픈 건 싫어!\n"
                           f"답변: [아픈 건 싫으니까 방어력에 올인하려고 합니다.\n"
                           f"질문: {user_question.answer}"
            }
        ]
        request_data = {
            "messages": preset_text,
            "topP": 0.8,
            "topK": 0,
            "maxTokens": 256,
            "temperature": 0.5,
            "repeatPenalty": 5.0,
            "stopBefore": [],
            "includeAiFilters": True,
            "seed": 141
        }

        # Clova API 실행
        response = completion_executor.execute(request_data)
        line = response[-4] # <- 이렇게 손수 만든 티를 내도 되는지? 더 똑똑한 방식이 있는지?
        # print(line)

        # 응답 데이터에서 title, description만 추출 
        if line.startswith("data:"):
            data = json.loads(line[5:])
            # print(data)
            # print(33)
            if "message" in data and "content" in data["message"]:
                content = data["message"]["content"]
                print(content)
                    
                match = re.search(r'답변: ["(.*?)"]\s+(.*)', content, re.DOTALL)
                print(22)
                # match = re.search(r'답변 : \["(.*?)"\]\((.*?)\) (.*)', content, re.DOTALL) <- 링크랑 같이 제거
                if match:
                    print(11)
                    title = match.group(1)  # 책 제목
                    # link = match.group(2)  # 링크 추출 <- 버그 수정 필요
                    description = match.group(2)  # 설명 추출
                    print(title)
                    print(description)

                    # 세션에 저장
                    request.session["result"] = ClovaResponse(title=title, description=description).dict()
                    return {
                        "message": "Question processed successfully. Please proceed to the next page.",
                        "title": title,
                        "description": description
                    }
        print(title)
        raise HTTPException(status_code=500, detail="No valid response from Clova API.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Clova API: {e}")


@router.get("/api/result_txt", response_model=ClovaResponse)
async def get_result_txt(request: Request):
    try:
        result = request.session.get("result")
        if not result:
            raise HTTPException(status_code=404, detail="No result found. Please submit a question first.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching result text: {e}")

@router.get("/api/loading", response_model=KeywordResponse)
async def get_loading_keywords():
    try:
        keywords = ["keyword1", "keyword2", "keyword3"]
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching keywords: {e}")

@router.get("/api/result_img", response_model=ImageResponse)
async def get_result_img():
    try:
        image_base64 = ""
        return {"image": image_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching generated image: {e}")
