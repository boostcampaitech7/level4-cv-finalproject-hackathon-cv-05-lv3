import pandas as pd

# 기존 CSV 파일 경로와 새로운 CSV 파일 저장 경로
input_csv = '사서추천도서목록_utf8.csv'  # 기존 파일 이름
output_csv = 'dataset.csv'  # 결과 파일 이름

# CSV 파일 읽기
df = pd.read_csv(input_csv)

# "서명" 컬럼 값 처리:
# 1. 모든 값에서 양쪽 공백 및 " 제거
# 2. [값] 형식으로 변경
df['서명'] = df['서명'].apply(lambda x: f"User: [{x.strip().strip('\"')}]" if isinstance(x, str) else x)

# "서명" 컬럼 이름을 "Completion"으로 변경
df.rename(columns={'서명': 'Text'}, inplace=True)

# 새로운 "Text" 컬럼 생성 (빈 문자열로 초기화)
df['Completion'] = ''

# 정렬: "Text" -> "Completion"
df = df[['Text', 'Completion']]

# 결과를 새로운 CSV 파일로 저장
df.to_csv(output_csv, index=False, encoding='utf-8')

print(f"새로운 데이터셋이 {output_csv}에 저장되었습니다!")
