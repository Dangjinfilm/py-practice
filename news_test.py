import requests
from bs4 import BeautifulSoup

keyword = "프랜차이즈"
url = f"https://search.naver.com/search.naver?where=news&query={keyword}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

print("--- [디버깅 모드: 네이버가 숨겨놓은 기사 찾기] ---")

# 페이지 안의 '모든 링크(a 태그)'를 가져옵니다.
links = soup.find_all('a')

count = 0
for link in links:
    text = link.text.strip()
    
    # 텍스트가 15글자 이상이면 기사 제목일 확률이 매우 높습니다.
    if len(text) > 15: 
        print(f"[{count+1}] 발견된 텍스트: {text}")
        print(f"    링크 주소: {link.get('href')}\n")
        count += 1
        
        # 5개만 찾고 멈춥니다.
        if count == 5:
            break

if count == 0:
    print("앗, 15자 이상의 텍스트를 가진 링크조차 없습니다.")