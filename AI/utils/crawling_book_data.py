from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ChromeDriver 설정
chrome_driver_path = "./chromedriver/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# 저장할 데이터 리스트
books_list = []
books_data = []

try:
    numbers = list(range(1, 153))  # 1~152 페이지 반복

    # ✅ 1차 크롤링 (목록 페이지)
    for num in numbers:
        url = f"https://www.mcst.go.kr/kor/s_culture/book/bookList.jsp?pSeq=&pDetailSeq=&pMenuCd=0531000000&pCurrentPage={num}&pRegYear=0000&pRegMonth=00&pCategory=00&pSearchType=TITLE&pSearchWord="
        driver.get(url)

        # li 태그가 로딩될 때까지 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#content > div.contentWrap > ul > li"))
        )

        # 각 li 태그 가져오기
        book_items = driver.find_elements(By.CSS_SELECTOR, "#content > div.contentWrap > ul > li")

        for item in book_items:
            try:
                # 카테고리
                cate = item.find_element(By.CSS_SELECTOR, "div.text.boox p.cate").text

                # 책 제목
                title = item.find_element(By.CSS_SELECTOR, "div.text.boox p.title").text

                # 저/역자 및 출판사
                details = item.find_elements(By.CSS_SELECTOR, "div.text.boox ul.list03 li")

                author = ""
                publisher = ""

                for detail in details:
                    text = detail.text
                    if "저/역자" in text:
                        author = text.replace("저/역자:", "").strip()
                    elif "출판사" in text:
                        publisher = text.replace("출판사:", "").strip()

                # 상세보기 링크
                detail_link = item.find_element(By.CSS_SELECTOR, "a.go").get_attribute("href")

                # books_list에 저장
                books_list.append({
                    "카테고리": cate,
                    "제목": title,
                    "저/역자": author,
                    "출판사": publisher,
                    "상세보기 링크": detail_link
                })

            except Exception as e:
                print(f"❌ 목록 크롤링 실패: {e}")

        print(f"📄 Page {num}: {len(book_items)} books collected.")

    print(f"✅ 전체 {len(books_list)}개의 책 목록을 성공적으로 크롤링 완료!")

    # ✅ 2차 크롤링 (상세 페이지)
    for idx, book in enumerate(books_list):
        driver.get(book["상세보기 링크"])
        time.sleep(1)  # 페이지 로드 대기

        try:
            # 상세 페이지 설명 로딩 대기
            content_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#content > div.contentWrap > div.viewWarp.width2 > div.view_con")
                )
            )
            full_text = content_element.text.strip()  # 전체 텍스트 추출
        except:
            full_text = "설명 없음"  # 예외 처리

        # 📝 상세 설명을 섹션별로 나누기
        sections = {
            "사서의 추천 글": "",
            "저자 소개": "",
            "책 속 한 문장": "",
            "함께 읽으면 좋은 책": ""
        }

        current_section = "book_description"
        section_order = list(sections.keys())

        lines = full_text.split("\n")
        temp_text = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line in section_order:
                if current_section != "book_description":
                    sections[current_section] = "\n".join(temp_text).strip()
                current_section = line
                temp_text = []
            else:
                temp_text.append(line)

        # 마지막 섹션 저장
        if current_section != "book_description":
            sections[current_section] = "\n".join(temp_text).strip()

        # 만약 특정 섹션이 존재하지 않으면 book_description 전체 사용
        if any(sections.values()):
            book_description = ""
        else:
            book_description = full_text

        print({
            "카테고리": book["카테고리"],
            "제목": book["제목"],
            "저/역자": book["저/역자"],
            "출판사": book["출판사"],
            "상세보기 링크": book["상세보기 링크"],
            "책 설명": book_description,
            "사서의 추천 글": sections["사서의 추천 글"],
            "저자 소개": sections["저자 소개"],
            "책 속 한 문장": sections["책 속 한 문장"],
            "함께 읽으면 좋은 책": sections["함께 읽으면 좋은 책"]
        })

        # 최종 데이터 저장
        books_data.append({
            "카테고리": book["카테고리"],
            "제목": book["제목"],
            "저/역자": book["저/역자"],
            "출판사": book["출판사"],
            "상세보기 링크": book["상세보기 링크"],
            "책 설명": book_description,
            "사서의 추천 글": sections["사서의 추천 글"],
            "저자 소개": sections["저자 소개"],
            "책 속 한 문장": sections["책 속 한 문장"],
            "함께 읽으면 좋은 책": sections["함께 읽으면 좋은 책"]
        })

        print(f"✅ [{idx+1}/{len(books_list)}] {book['제목']} - 상세 크롤링 완료!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()  # Chrome 종료

    # 데이터프레임으로 변환 후 CSV 저장
    df = pd.DataFrame(books_data)
    df.to_csv("books_data.csv", index=False, encoding="utf-8-sig")
