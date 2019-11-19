import time
import threading
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import schedule

from scraping.scraping_func import views_scraping_func, rakuten_scraping_func, aoyama_scraping_func, epos_scraping_func, mizuhobank_scraping_func


def job():
    print("views")
    views_thread = threading.Thread(target=views_scraping_func)
    views_thread.start()
    
    print("rakuten")
    rakuten_thread = threading.Thread(target=rakuten_scraping_func)
    rakuten_thread.start()
    
    print("aoyama")
    aoyama_thread = threading.Thread(target=aoyama_scraping_func)
    aoyama_thread.start()
    
    print("epos")
    epos_thread = threading.Thread(target=epos_scraping_func)
    epos_thread.start()
    
    print("mizuhobank")
    mizuhobank_thread = threading.Thread(target=mizuhobank_scraping_func)
    mizuhobank_thread.start()

# test
# schedule.every(10).minutes.do(job)

# 月曜日と金曜日にjobを実行
schedule.every().monday.do(job)
schedule.every().friday.do(job)

# 10:30に実行
# schedule.every().day.at("10:30").do(job)

# 水曜日の13:15にjobを実行
# schedule.every().wednesday.at("13:15").do(job)


while True:
    schedule.run_pending()
    time.sleep(50)