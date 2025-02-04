from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 저장 경로 설정
OUTPUT_PATH = "~/new_books.xlsx"  # 필요에 맞게 변경
VECTOR_DB_PATH = "~/vector_db.index"  # 벡터 DB 저장 경로

# 1️⃣ 엑셀 다운로드 함수
def download_excel():
    url = "https://kobic.net/book/newBook/excel.do"
    response = requests.get(url)
    if response.status_code == 200:
        with open(OUTPUT_PATH, "wb") as f:
            f.write(response.content)
        print(f"File downloaded and saved to {OUTPUT_PATH}")
    else:
        raise Exception("Failed to download file.")

# 2️⃣ 벡터 DB 생성 함수
def process_excel_and_store_vectors():
    # 엑셀 파일 로드
    df = pd.read_excel(OUTPUT_PATH, usecols=["C"], skiprows=4, nrows=3331)
    book_titles = df.iloc[:, 0].dropna().tolist()
    
    # 문장 임베딩 모델 로드
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(book_titles, convert_to_numpy=True)
    
    # FAISS 벡터 DB 생성 및 저장
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, VECTOR_DB_PATH)
    
    print(f"Vector DB saved to {VECTOR_DB_PATH}")

# 3️⃣ Airflow DAG 정의
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "download_and_process_excel",
    default_args=default_args,
    description="Download Excel file weekly and process into Vector DB",
    schedule_interval="0 0 * * 1",  # 매주 월요일 00:00 실행
    catchup=False,
)

# 4️⃣ DAG Task 정의
download_task = PythonOperator(
    task_id="download_excel_file",
    python_callable=download_excel,
    dag=dag,
)

process_task = PythonOperator(
    task_id="process_excel_and_store_vectors",
    python_callable=process_excel_and_store_vectors,
    dag=dag,
)

# 5️⃣ Task 실행 순서 지정
download_task >> process_task
