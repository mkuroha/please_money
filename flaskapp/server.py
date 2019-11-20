import datetime
import threading
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import psycopg2
import datetime
from datetime import datetime as dt
from flask import Flask, render_template, redirect
from joblib import Parallel, delayed  # マルチスレッド

from scraping.scraping_func import views_scraping_func, rakuten_scraping_func, aoyama_scraping_func, epos_scraping_func, mizuhobank_scraping_func
from lib.utils import calc_bank_balance, extract_close_payment


app = Flask(__name__)


@app.route("/")
def index():
    # データベースから直近のデータだけ取り出し，支払い額を計算してtemplateに渡す
    # データベース接続
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    cur.execute("SELECT * FROM payment")
    payment = cur.fetchall()
    cur.execute("SELECT * FROM bank")
    bank = cur.fetchall()
    
    now_date = dt.now()
    now_date_str = now_date.strftime("%Y/%m/%d")
    
    # 口座残高の計算
    bank_balance = calc_bank_balance(bank)
    
    # 支払日算出，分割払いの計算，直近の支払い情報の抽出
    alldata, neardata = extract_close_payment(payment)
    
    
    # 和の計算
    # 直近の支払日の計算
    sum_list = [["2019/11/3", 1200], ["2019/11/4", 1500],  ["2019/11/5", 20000]]
    all_sum = 22700

    return render_template(
        "index.html", 
        title="Please Money", 
        today=now_date_str,
        sum_list=sum_list,
        all_sum=all_sum,
        # payment_date_list=payment_date_list,
        # views=views_payment_sum, 
        # rakuten=rakuten_payment_sum,
        # epos=epos_payment_sum,
        # aoyama=aoyama_payment_sum,
        bank_balance=bank_balance,
        # bonus=views_bonus_value
        )
    

if __name__ == "__main__":
    app.run(debug=True)