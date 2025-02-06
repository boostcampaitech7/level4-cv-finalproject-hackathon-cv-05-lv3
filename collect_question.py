import os
import sys
import urllib.request
import requests
from bs4 import BeautifulSoup
import csv
import json

client_id = ""
client_secret = ""
encText = urllib.parse.quote("책추천")
url = "https://openapi.naver.com/v1/search/kin.json?query=" + encText + "&display=100&start=1"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

all_data = [['제목', '질문내용']]

for start in range(1, 10):
    url = f"https://openapi.naver.com/v1/search/kin.json?query={encText}&display=100&start={start}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))
        
        for item in data['items']:
            detail_url = item['link']
            response = requests.get(detail_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title_div = soup.select_one('.endTitleSection')
            if title_div:
                icon_span = title_div.find('span', class_='iconQuestion')
                if icon_span:
                    icon_span.extract() 
                title = title_div.get_text(strip=True)
            else:
                title = ""

            content_div = soup.select_one('div.questionDetail')
            question_content = content_div.get_text('\n', strip=True) if content_div else ""

            all_data.append([title, question_content])

    else:
        print("Error Code:" + str(rescode))

with open('result.csv', 'w', newline='', encoding='utf-8-sig') as f:
    csv.writer(f).writerows(all_data)

print("크롤링 완료")
