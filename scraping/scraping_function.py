import json

from .lib.get_html import views_selenium, mizuhobank_selenium, rakuten_selenium, epos_selenium, aoyama_selenium
from .lib.extract_content import views_scraping, mizuhobank_scraping, rakuten_scraping, epos_scraping, aoyama_scraping

"""
extract_content.pyの関数から，使用情報のリストが渡されるため，その情報が新しい場合，データベースに格納する
"""

def views_scraping_func():
    views_html = views_selenium()
    views_scraping(views_html)


def rakuten_scraping_func():
    rakuten_html = rakuten_selenium()
    rakuten_scraping(rakuten_html)


def aoyama_scraping_func():
    aoyama_html = aoyama_selenium()
    aoyama_scraping(aoyama_html)


def epos_scraping_func():
    epos_html = epos_selenium()
    epos_scraping(epos_html)


def mizuhobank_scraping_func():
    mizuhobank_html = mizuhobank_selenium()
    mizuhobank_scraping(mizuhobank_html)


if __name__ == "__main__":
    pass