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
    bank_list = []
    for eachdata in bank:
        tmp_list = []
        for i in range(len(eachdata)):
            tmp_list.append(eachdata[i])
        
        tmp_list[1] = tmp_list[1].strftime("%Y/%m/%d")
        bank_list.append(tmp_list)
    
    # 支払日算出，分割払いの計算，直近の支払い情報の抽出
    alldata, neardata = extract_close_payment(payment)
    
    views = []
    rakuten = []
    aoyama = []
    epos = []
    date_list = []
    for eachdata in neardata:
        eachdata[0] = eachdata[0].strftime("%Y/%m/%d")
        eachdata[5] = eachdata[5].strftime("%Y/%m/%d")
        if not (eachdata[5] in date_list):
            date_list.append(eachdata[5])
        
        if eachdata[1]=="Views":
            views.append(eachdata)
        elif eachdata[1]=="Rakuten":
            rakuten.append(eachdata)
        elif eachdata[1]=="Aoyama":
            aoyama.append(eachdata)
        else:
            epos.append(eachdata)
    
    # 同じ日付の合計を計算
    payment_sum_list_by_date = [0 for _ in range(len(date_list))]  # 支払日ごとの金額の合計を格納するためのもの
    for eachdata in neardata:
        # 全ての日付をfor文で回し，一致したものについて金額を足す
        for i in range(len(date_list)):
            if date_list[i]==eachdata[5]:
                payment_sum_list_by_date[i] += eachdata[2]
    
    # 日付と支払額の合計のtupleを作成する
    payment_date_and_value = list( zip(date_list, payment_sum_list_by_date) )
    
    # 和の計算
    all_sum = sum(payment_sum_list_by_date)
    
    
    return render_template(
        "index.html", 
        title="Please Money", 
        today=now_date_str,
        sum_list=payment_date_and_value,
        all_sum=all_sum,
        view_list=views, 
        rakuten_list=rakuten,
        aoyama_list=aoyama,
        epos_list=epos,
        bank_balance=bank_balance,
        bank_list=bank_list,
        )
    

if __name__ == "__main__":
    app.run(debug=True)