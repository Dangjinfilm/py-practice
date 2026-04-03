import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 대시보드 기본 설정
st.set_page_config(page_title="외식업 트렌드 모니터링", layout="wide")

# 2. 화면 상단 제목 및 설명 (원하시는 대로 수정 가능합니다)
st.title("📊 새모양 F&B 뉴스 모니터링 대시보드")
st.write("달빛에구운고등어, 얌스, 만수식당 브랜드 마케팅 및 시장 조사를 위한 뉴스 자동 수집기입니다.")
st.markdown("---")

# 3. 사이드바에 검색창 만들기
st.sidebar.header("검색 설정")
keyword = st.sidebar.text_input("검색어를 입력하세요", "외식업 창업")

# 4. '뉴스 가져오기' 버튼이 눌렸을 때 실행될 동작
if st.button(f"'{keyword}' 뉴스 가져오기"):
    with st.spinner('뉴스를 수집하고 있습니다. 잠시만 기다려주세요...'):
        
        # 앞서 성공했던 네이버 크롤링 로직
        url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        
        news_list = []
        for link in links:
            text = link.text.strip()
            # 15자 이상인 텍스트만 추출하여 리스트에 담기 (최대 10개)
            if len(text) > 15:
                news_list.append({
                    "기사 제목": text, 
                    "뉴스 링크": link.get('href')
                })
                if len(news_list) >= 10: 
                    break
        
        # 5. 수집된 데이터를 화면에 예쁜 표로 출력하기
        if news_list:
            df = pd.DataFrame(news_list) # 리스트를 판다스 데이터프레임(표 형식)으로 변환
            st.success("뉴스 수집 완료!")
            st.dataframe(df, use_container_width=True) # 대시보드에 표 그리기
        else:
            st.error("뉴스를 찾지 못했습니다. 다른 검색어를 입력해 보세요.")