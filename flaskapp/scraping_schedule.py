import time
import threading
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import schedule
import psycopg2

from scraping.scraping_func import views_scraping_func, rakuten_scraping_func, aoyama_scraping_func, epos_scraping_func, mizuhobank_scraping_func
from lib.utils import calc_bank_balance, extract_close_payment
from lib.push_line import push_line


def job():
    views_thread = threading.Thread(target=views_scraping_func)
    views_thread.start()
    
    rakuten_thread = threading.Thread(target=rakuten_scraping_func)
    rakuten_thread.start()
    
    aoyama_thread = threading.Thread(target=aoyama_scraping_func)
    aoyama_thread.start()
    
    epos_thread = threading.Thread(target=epos_scraping_func)
    epos_thread.start()
    
    mizuhobank_thread = threading.Thread(target=mizuhobank_scraping_func)
    mizuhobank_thread.start()
    
    
    # threadが終わるのを待つ
    thread_list = threading.enumerate()
    thread_list.remove(threading.main_thread())
    for thread in thread_list:
        thread.join()
    
    # 残高と支払額の差を計算し，ある値以上のときLINEに通知する
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    cur.execute("SELECT * FROM payment")
    payment = cur.fetchall()
    cur.execute("SELECT * FROM bank")
    bank = cur.fetchall()
    
    bank_balance = calc_bank_balance(bank)
    alldata, neardata = extract_close_payment(payment)
    all_sum = 0
    for eachdata in neardata:
        all_sum += eachdata[2]
    
    if (all_sum - bank_balance) > 50000:
        push_line("Please Money \n 銀行残高： {} 円，支払額： {} 円 で金額が不足しています，".format(bank_balance, all_sum))


# 月曜日と水曜日と金曜日と日曜日にjobを実行
schedule.every().monday.do(job)
schedule.every().wednesday.do(job)
schedule.every().friday.do(job)
schedule.every().sunday.do(job)


while True:
    schedule.run_pending()
    time.sleep(50)