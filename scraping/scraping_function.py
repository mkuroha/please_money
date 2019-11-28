import json

from .lib.get_html import views_selenium, mizuhobank_selenium, rakuten_selenium, epos_selenium, aoyama_selenium
from .lib.extract_content import views_scraping, mizuhobank_scraping, rakuten_scraping, epos_scraping, aoyama_scraping

# from lib.get_html import views_selenium, mizuhobank_selenium, rakuten_selenium, epos_selenium, aoyama_selenium
# from lib.extract_content import views_scraping, mizuhobank_scraping, rakuten_scraping, epos_scraping, aoyama_scraping

"""
extract_content.pyの関数から，使用情報のリストが渡されるため，その情報が新しい場合，データベースに格納する
"""

def views_scraping_func():
    print("--------------------------------- views selenium ---------------------------------")
    views_html = views_selenium()
    print("--------------------------------- views scraping ---------------------------------")
    views_scraping(views_html)


def rakuten_scraping_func():
    print("--------------------------------- rakuten selenium --------------------------------")
    rakuten_html = rakuten_selenium()
    print("--------------------------------- rakuten scraping --------------------------------")
    rakuten_scraping(rakuten_html)


def aoyama_scraping_func():
    print("--------------------------------- aoyama selenium ---------------------------------")
    aoyama_html = aoyama_selenium()
    print("--------------------------------- aoyama scraping ---------------------------------")
    aoyama_scraping(aoyama_html)


def epos_scraping_func():
    print("--------------------------------- epos selenium ----------------------------------")
    epos_html = epos_selenium()
    print("--------------------------------- epos scraping ----------------------------------")
    epos_scraping(epos_html)


def mizuhobank_scraping_func():
    print("---------------------------------- mizuhobank selenium ----------------------------------")
    mizuhobank_html = mizuhobank_selenium()
    print("---------------------------------- mizuhobank scraping ----------------------------------")
    mizuhobank_scraping(mizuhobank_html)


if __name__ == "__main__":
    views_scraping_func()
    rakuten_scraping_func()
    aoyama_scraping_func()
    epos_scraping_func()
    mizuhobank_scraping_func()