# スクレイピングを実行する関数
# Herokuで定期実行ができるらしい ( https://qiita.com/seigo-pon/items/ca9951dac0b7fa29cce0 )
import time
# import psycopg2

from .get_html import views_selenium, mizuhobank_selenium, rakuten_selenium, epos_selenium, aoyama_selenium
from .extract_content import views_scraping, mizuhobank_scraping, rakuten_scraping, epos_scraping, aoyama_scraping
# from .push_line import push_line


def main():
    views_html = views_selenium()
    views_contents = views_scraping(views_html)
    
    mizuhobank_html = mizuhobank_selenium()
    mizuhobank_contents = mizuhobank_scraping()
    
    rakuten_html = rakuten_selenium()
    rakuten_contents = rakuten_scraping()

    epos_html = epos_selenium()
    epos_contents = epos_scraping()
    
    aoyama_html = aoyama_selenium()
    aoyaman_contents = aoyama_scraping()
    
    
if __name__ == "__main__":
    main()