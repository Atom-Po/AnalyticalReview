import pandas as pd
from fuzzywuzzy import process

stockCode_df = pd.read_csv(r'db\stockCode.csv', encoding='cp949')

def find_similar_code(search_term):
    # "한글 종목명" 열에서 가장 유사한 값 찾기
    match = process.extractOne(search_term, stockCode_df["한글 종목명"])
    
    # 가장 유사한 값의 인덱스를 찾고 "단축코드" 값 반환
    if match:
        matched_index = stockCode_df[stockCode_df["한글 종목명"] == match[0]].index[0]
        return search_term, stockCode_df.loc[matched_index, "단축코드"]
    else:
        return None  # 유사한 값을 찾지 못한 경우 None 반환

if __name__ == '__main__':
    finded_name, finded_code = find_similar_code('희림종합건축')
    print(finded_name)
    print(finded_code)