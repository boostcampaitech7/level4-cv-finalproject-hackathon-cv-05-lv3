import requests
import json
import csv
import pandas as pd
#api 아이디와 비밀번호 작성
client_ids = [
]
client_secrets = [
]

csv_file_path = '/data/ephemeral/home/NL_BO_BOOK_PUB_202403-1.csv'
try:
    df = pd.read_csv(csv_file_path, usecols=['TITLE_NM'], skiprows=0, nrows=758083)
    #df = df[:99996]#1차
    #df = df[99996:199996]#2차
    #df = df[199996:299996]#3차
    #df = df[299996:399996]#4차
    #df = df[399996:499996]#5차
    #df = df[499996:599996]#6차
    #df = df[599996:699996]#7차
    df = df[699996:]#8차
    if df.empty:
        print("csv 파일에서 데이터를 읽지 못했습니다. 작업을 종료합니다.")
        exit()
except Exception as e:
    print(f"csv 파일을 읽는 중 오류 발생: {e}")
    exit()

# 책 제목 목록 생성
book_titles = df.iloc[:, 0].dropna().tolist()

csv_data = []

for i, title in enumerate(book_titles):
    query = title
    url = f"https://openapi.naver.com/v1/search/book.json?query={query}&display=1&start=1"
    client_index = i % len(client_ids)
    print(i,"/100000")
    headers = {
        "X-Naver-Client-Id": client_ids[client_index],
        "X-Naver-Client-Secret": client_secrets[client_index]
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        for item in data.get('items', []):
            book_title = item.get('title', '').replace(',', ' ')
            author = item.get('author', '').replace(',', ' ')
            publisher = item.get('publisher', '').replace(',', ' ')
            pubdate = item.get('pubdate', '')
            isbn = item.get('isbn', '')
            description = item.get('description', '').replace(',', ' ')
            link = item.get('link', '')
            image = item.get('image', '')
            book_info = f"책 제목 : {book_title} \n저자 : {author}\n출판사 : {publisher}\n출판일 : {pubdate}\nISBN : {isbn}\n설명 : {description}\n섬네일 링크 : {image}\n구매링크 : {link}"
            csv_data.append([book_title, book_info])
    else:
        print(f"API 요청 실패: {response.status_code}")
        
with open('book_info6차.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Book Title", "Final Answer"])
    writer.writerows(csv_data)

print("CSV 파일이 성공적으로 생성되었습니다.")
