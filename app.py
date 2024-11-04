import FS_crawler
import stock_searcher

if __name__ == '__main__':
    find_name, find_code = stock_searcher.find_similar_code('삼성전자')
    print(f'find_name : {find_name}, find_code : {find_code}')
    fs_df = FS_crawler.FS_crawler(find_code)
    print(fs_df)