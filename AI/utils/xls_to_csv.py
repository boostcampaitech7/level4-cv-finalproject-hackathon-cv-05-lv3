import pyexcel as p

# xls 파일 경로와 csv 파일 저장 경로
xls_file = '사서추천도서 목록_2025-01-26.xls'  # 변환할 xls 파일 경로
csv_file = '사서추천도서목록_utf8.csv'  # 저장할 csv 파일 경로

# xls 파일 읽고 csv로 저장
sheet = p.get_sheet(file_name=xls_file)
sheet.save_as(csv_file)

print(f"{csv_file} 파일로 저장되었습니다!")
