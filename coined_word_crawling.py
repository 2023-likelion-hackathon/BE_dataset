import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def crawl_list_items(url):
    # 웹 페이지에 GET 요청 보내기
    response = requests.get(url)

    # 웹 페이지의 HTML 내용 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # <li> 태그 안에 있는 값을 추출
    li_items = []



    for li_tag in soup.find_all('li'):
        item_arr =[] # 크롤링 데이터
        pattern = r'\[\d+\]' # 필터링 용 정규 표현식 패턴

        # 신조어 단어
        btag_item = li_tag.find('b')
        b_text = btag_item.text.strip() if btag_item else ""
        if b_text =="" : continue

        # 신조어 설명 문자열
        text_item = li_tag.text.strip()
        if text_item is None:
            text_item = ""
        else: text_item = re.sub(pattern, '', text_item) # 불필요한 문자열 제거


        #신조어 url
        atag_item = btag_item.find('a')
        item_url = atag_item.get('href') if atag_item else ""

        item_arr.append(b_text)
        item_arr.append(text_item)
        if item_url!="" : item_arr.append(item_url)

        li_items.append(item_arr)

    return li_items


if __name__ == '__main__':
    # 위키백과 대한민국 인터넷 신조어 목록
    url = "https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%9D%B8%ED%84%B0%EB%84%B7_%EC%8B%A0%EC%A1%B0%EC%96%B4_%EB%AA%A9%EB%A1%9D"
    items = crawl_list_items(url)
    for item in items:
        print(item)
    header = ['word','meaning','url']
    df = pd.DataFrame(items)

    output_file = "dataset/coined_word.xlsx"
    df.to_excel(output_file,index=False,header=header)