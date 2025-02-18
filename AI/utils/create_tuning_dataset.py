import os
import pandas as pd

# 현재 작업 디렉토리 확인
current_dir = os.getcwd()
# 상대 경로에서 파일 경로 설정
csv_path = os.path.join(current_dir, "dataset_ver2_augm.csv")
# CSV 파일 불러오기
books = pd.read_csv(csv_path)

# 데이터셋에 필요한 컬럼이 있는지 확인
expected_columns = ["Text", "Completion"]
if not all(col in books.columns for col in expected_columns):
    raise ValueError("데이터셋에는 'Text'와 'Completion' 컬럼이 포함되어 있어야 합니다.")

# 필요한 컬럼 생성
books["System_Prompt"] = "- 당신은 지식이 풍부한 도서 큐레이터입니다.\n- 사용자의 나이 :  10대, 성별 : 남성\n- 사용자의 질문에 대해 사용자의 나이, 성별을 분석하여 시중에 있는 책에서 관련 내용을 인용하거나 추천하는 방식으로 답변합니다.\n- 사용자의 질의를 분석하고 질의와 상관관계를 보이는 책 제목으로 답해줘\n- 1개의 답변이고, 명확하고 간결하며, 독자가 흥미를 느낄 수 있도록 작성하세요."
books["C_ID"] = range(len(books))  # 0부터 시작하는 증가하는 인덱스 생성
books["T_ID"] = 0  # 모든 행에 대해 T_ID를 0으로 설정

# 컬럼 순서 재정렬
books = books[["System_Prompt", "C_ID", "T_ID", "Text", "Completion"]]

# 변환된 데이터 저장
output_file_path = "processed_dataset_ver2_augm.csv"
books.to_csv(output_file_path, index=False)