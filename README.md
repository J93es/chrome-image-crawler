# img_crawler

- 구글 드라이버를 이용한 이미지 크롤러 입니다.

# 사용법

1. 환경 설정

   - 파이썬에서 selenium, time, csv, numpy, urllib.request를 사용할 수 있어야 합니다.
   - 사용자 pc와 크롬 버전에 호환되는 chromedriver의 설치가 필요합니다. (https://chromedriver.chromium.org/downloads)
     - "다운 받은 chromedriver"를 "현재 git에 존재하는 chromedriver"와 교체하세요. (디렉토리 구조는 당연히 변하면 안됩니당)

2. img_urls_crawler.py 파일 및 디렉토리 구성

   - img_urls_crawler.py에서 """ custom this place """ 문구를 찾고 targetName(검색어), fileName(파일 명), maxLen(수집할 이미지의 최대 개수)를 설정합니다.
   - img_urls/{fileName}/{fileName}.csv 및 img_urls/{fileName}/{fileName}\_bak.csv의 디렉토리가 존재해야 합니다.

3. img_srcs_saver.py 파일 및 디렉토리 구성

   - img_srcs_saver.py에서 """ custom this place """ 문구를 찾고 fileName(파일 명)을 설정합니다.
   - img_srcs/fileName/ 디렉토리가 존재해야 합니다.

# 기타 문제 해결

1.  Xpath 관련 문제

    - img_urls_crawler.py에서 """ Xpath """ 문구를 찾는다.
    - 크롬에서 다운받고자 하는 이미지에서 우클릭 > 검사 > 하이라이트 되어있는 코드에서 우클릭 > copy > copy full Xpath 후 파이썬 코드에 붙여넣는다.

2.  브라우저 권한 설정 관련 문제(404에러 등)

    - img_urls_crawler.py와 img_srcs_saver.py에서 """ browser header setting """ 문구를 찾는다.
    - header에 권한 관련 내용을 추가한다.
