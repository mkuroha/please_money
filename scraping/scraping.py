# スクレイピングを実行する関数
# Herokuで定期実行ができるらしい ( https://qiita.com/seigo-pon/items/ca9951dac0b7fa29cce0 )
import time
# import psycopg2

from get_html import views_selenium, mizuhobank_selenium, rakuten_selenium, epos_selenium, aoyama_selenium
from extract_content import views_scraping, mizuhobank_scraping, rakuten_scraping, epos_scraping, aoyama_scraping
# from .push_line import push_line


def main():
    print("start views selenium\n---------------------------------------------------------------------")
    views_html = views_selenium()
    print("start views scraping\n---------------------------------------------------------------------")
    
    views_contents = views_scraping(views_html)
    print("start mizuhobank selenium\n---------------------------------------------------------------------")
    mizuhobank_html = mizuhobank_selenium()
    print("start mizuhobank scraping\n---------------------------------------------------------------------")
    mizuhobank_contents = mizuhobank_scraping(mizuhobank_html)
    
    print("start rakuten selenium\n---------------------------------------------------------------------")
    rakuten_html = rakuten_selenium()
    print("start rakuten selenium\n---------------------------------------------------------------------")
    rakuten_contents = rakuten_scraping(rakuten_html)
    
    print("start epos selenium\n---------------------------------------------------------------------")
    epos_html = epos_selenium()
    print("start epos selenium\n---------------------------------------------------------------------")
    epos_contents = epos_scraping(epos_html)
    
    print("start aoyama selenium\n---------------------------------------------------------------------")
    aoyama_html = aoyama_selenium()
    print("start aoyama selenium\n---------------------------------------------------------------------")
    aoyaman_contents = aoyama_scraping(aoyama_html)
    
    
if __name__ == "__main__":
    main()