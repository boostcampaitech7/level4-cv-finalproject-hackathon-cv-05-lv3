import pandas as pd
import json
from deepeval.metrics import AnswerRelevancyMetric,PromptAlignmentMetric
from deepeval.test_case import LLMTestCase
from langchain_ollama.llms import OllamaLLM
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.metrics import HallucinationMetric
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
import json
from tqdm import tqdm
import matplotlib as plt
import time
import pynvml
import gc
import torch
from numba import cuda

# GPU 메모리 모니터링 함수
def get_gpu_memory():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return info.used / (1024 ** 3)  # GB 단위

# 모델 관리 클래스
class ModelManager:
    def __init__(self):
        self.llm = None
        self.wrapped_model = None
        
    def initialize(self):
        self.llm = OllamaLLM(model='huihui_ai/deepseek-r1-abliterated:32b', temperature=0.3)
        self.wrapped_model = OllamaWrapper(self.llm)
        
    def release(self):
        del self.llm, self.wrapped_model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        cuda.select_device(0)
        cuda.close()
        time.sleep(3)
# 로거 설정
def setup_logger():
    logger = logging.getLogger("EvaluationLogger")
    logger.setLevel(logging.DEBUG)

    # 파일 핸들러 (50MB 회전, 최대 5개 파일 보관)
    file_handler = RotatingFileHandler(
        'evaluation.log',
        maxBytes=50*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()
class TqdmLoggingHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
        except Exception:
            self.handleError(record)

# tqdm과 통합된 로깅 핸들러 추가
tqdm_handler = TqdmLoggingHandler()
tqdm_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(tqdm_handler)
class OllamaWrapper(DeepEvalBaseLLM):
    def __init__(self, model):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        return self.model.invoke(prompt)

    async def a_generate(self, prompt: str) -> str:
        return await self.model.ainvoke(prompt)

    def get_model_name(self):
        return "huihui_ai/deepseek-r1-abliterated:32b"
def process_csv(input_path, output_path):
    try:
        #logger.info(f"CSV 파일 로드 시작: {input_path}")
        df = pd.read_csv(input_path)
        #df=df[:100]
        #df=df[45:100]
        #logger.info(f"성공적으로 로드된 행 수: {len(df)}")
        
    except FileNotFoundError:
        logger.error("CSV 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
        raise
    except Exception as e:
        logger.error(f"CSV 로드 중 오류 발생: {str(e)}")
        raise

    results = []
    llm = OllamaLLM(model='huihui_ai/deepseek-r1-abliterated:32b', temperature=0.3)
    wrapped_model = OllamaWrapper(llm)

    # tqdm 진행률 표시기 설정 (검색 결과 [23][46] 참조)
    model_manager = ModelManager()
    model_manager.initialize()
    
    with tqdm(total=len(df), desc="행 처리 진행률", unit="row") as pbar:
        for index, row in df.iterrows():
            try:
                # GPU 메모리 체크 (10GB 기준)
                if get_gpu_memory() > 10:
                    logger.warning("GPU 메모리 초기화 시작")
                    model_manager.release()
                    model_manager.initialize()
                response_data = json.loads(row['응답'])
                actual_output = response_data['result']['message']['content']
                
                # 테스트 케이스 생성
                test_case = LLMTestCase(
                input=row['질문'],
                actual_output=actual_output,
                expected_output=response_data['result']['message']['content'],
                )
                # 지표 평가
                metrics = {
                    'AnswerRelevancy': AnswerRelevancyMetric(threshold=0.7, model=wrapped_model),
                    'PromptAlignmentMetric' : PromptAlignmentMetric(model=wrapped_model,prompt_instructions='''
                        "추천 도서 목록에서 가장 적합한 1권만 선정해야 함", 
                        "추천 이유를 자연스러운 문체로 설명해야 함",
                        "추천도서 정보 외 다른 출처를 사용하지 말아야 함",
                        "욕설이나 사용자에게 폭력적인 내용이 포함되어 있지 않은가",
                        "답변의 전반적인 품질이 좋은가",
                        "문법적으로 완벽한가"
                        ''')
                }

                max_retries = 100
                retry_delay = 0  # 초 단위 재시도 간격

                for name, metric in metrics.items():
                    success = False
                    for attempt in range(max_retries):
                        try:
                            metric.measure(test_case)
                            success = True
                            break
                        except ValueError as e:
                            if "invalid JSON" in str(e) and attempt < max_retries - 1:
                                logger.warning(f"행 {index+1} {name} 측정 실패 ({attempt+1}차 재시도)...")
                                time.sleep(retry_delay)
                                continue
                            else:
                                logger.error(f"행 {index+1} {name} 측정 최종 실패: {str(e)}")
                                
                                results.append({
                                    'Question': row['질문'],
                                    'Metric': name,
                                    'Score': 0.0,
                                    'Reason': f"평가 실패: {str(e)}",
                                    'Actual Output': actual_output
                                })
                                
                    if success:
                        results.append({
                            'Question': row['질문'],
                            'Metric': name,
                            'Score': metric.score,
                            'Reason': metric.reason,
                            'Actual Output': actual_output
                        })

                pbar.set_postfix_str(f"최근 점수: {metric.score:.2f}")
                pbar.update(1)

            except json.JSONDecodeError:
                logger.warning(f"행 {index+1} JSON 파싱 오류 - 건너뜀")
                pbar.update(1)
                continue
            
            except Exception as e:
                logger.error(f"행 {index+1} 처리 중 오류: {str(e)}")
                model_manager.release()
                model_manager.initialize()
                continue
    # 결과 저장
    try:
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_path, index=False)
        logger.info(f"평가 결과 저장 완료: {output_path}")
    except Exception as e:
        logger.error(f"결과 저장 실패: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        process_csv(
            input_path='result_question_answer.csv',
            output_path='evaluation_results2.csv'
        )
    except Exception as e:
        logger.critical(f"프로세스 실패: {str(e)}")
        raise