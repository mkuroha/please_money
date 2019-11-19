import json

from .get_html import views_selenium, mizuhobank_selenium, rakuten_selenium, epos_selenium, aoyama_selenium
from .extract_content import views_scraping, mizuhobank_scraping, rakuten_scraping, epos_scraping, aoyama_scraping

"""
extract_content.pyの関数から，使用情報のリストが渡されるため，その情報が新しい場合，データベースに格納する
# TODO: jsonに出力ではなくデータベースに保存に変更
"""

def views_scraping_func():
    views_html = views_selenium()
    views_contents_tmp = views_scraping(views_html)
    with open("./json/views_contents.json", "w") as fw:
        json.dump(views_contents_tmp, fw, indent=4)

def rakuten_scraping_func():
    rakuten_html = rakuten_selenium()
    rakuten_contents_tmp = rakuten_scraping(rakuten_html)
    with open("./json/rakuten_contents.json", "w") as fw:
        json.dump(rakuten_contents_tmp, fw, indent=4)

def aoyama_scraping_func():
    aoyama_html = aoyama_selenium()
    aoyama_contents_tmp = aoyama_scraping(aoyama_html)
    with open("./json/aoyama_contents.json", "w") as fw:
        json.dump(aoyama_contents_tmp, fw, indent=4)

def epos_scraping_func():
    epos_html = epos_selenium()
    epos_contents_tmp = epos_scraping(epos_html)
    with open("./json/epos_contents.json", "w") as fw:
        json.dump(epos_contents_tmp, fw, indent=4)

def mizuhobank_scraping_func():
    mizuhobank_html = mizuhobank_selenium()
    mizuhobank_balance = mizuhobank_scraping(mizuhobank_html)
    with open("./json/mizuhobank_balance.json", "w") as fw:
        json.dump(mizuhobank_balance, fw, indent=4)


if __name__ == "__main__":
    pass