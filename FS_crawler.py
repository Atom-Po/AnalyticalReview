import pandas as pd
import requests
import re

def FS_crawler(code):
    '''네이버증권에서 재무정보를 스크래핑'''

    # "encparam" 값을 추출하기 위한 정규 표현식 패턴 설정함
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    # "id" 값을 추출하기 위한 정규 표현식 패턴 설정함
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)
    
    # 회사 코드(code)를 기반으로 네이버 증권의 회사 정보 페이지 URL 생성함
    url = "http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code)
    # 해당 URL에 요청을 보내 HTML 텍스트 가져옴
    html = requests.get(url).text
    # 정규 표현식을 사용해 HTML에서 "encparam" 값을 추출함
    encparam = re_enc.search(html).group(1)
    # 정규 표현식을 사용해 HTML에서 "id" 값을 추출함
    encid = re_id.search(html).group(1)
    
    # 추출한 정보(encparam, id)를 포함하여 재무 정보 AJAX 요청 URL 생성함
    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(code, encparam, encid)
    # HTTP 요청 헤더에 Referer 값을 설정하여 해당 URL에 요청 보냄
    headers = {"Referer": "HACK"}
    # AJAX URL에 요청을 보내 HTML 텍스트 가져옴
    html = requests.get(url, headers=headers).text
    # print(html)  # HTML 내용 확인용으로 주석 처리된 코드임
    
    # HTML에서 표 데이터를 추출하여 데이터프레임 목록으로 반환함
    dfs = pd.read_html(html)
    # 추출한 데이터프레임 중 두 번째 표를 선택하고 "연간연간컨센서스보기" 열을 가져옴
    df = dfs[1]['연간연간컨센서스보기']
    # 인덱스를 "주요재무정보" 열의 값으로 설정함
    df.index = dfs[1]['주요재무정보'].values.flatten()
    
    # 재무 정보를 담은 데이터프레임 반환함
    return df


if __name__ == '__main__':
    df = FS_crawler("058610")
    print(df)