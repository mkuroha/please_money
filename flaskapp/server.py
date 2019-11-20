import datetime
import threading
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import psycopg2
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
    
    # 口座残高の計算
    bank_balance = calc_bank_balance(bank)
    
    # 支払日算出，分割払いの計算，直近の支払い情報の抽出
    alldata, neardata = extract_close_payment(payment)
    
    
    # with open("json/views_contents.json", "r") as fr:
    #     views_contents = json.load(fr)
    # views_payment_sum, views_bonus_value = calc_payment_sum(views_contents, "views")
    
    # with open("json/rakuten_contents.json", "r") as fr:
    #     rakuten_contents = json.load(fr)
    # rakuten_payment_sum = calc_payment_sum(rakuten_contents, "rakuten")
    
    # with open("json/epos_contents.json", "r") as fr:
    #     epos_contents = json.load(fr)
    # epos_payment_sum = calc_payment_sum(epos_contents, "epos")
    
    # with open("json/aoyama_contents.json", "r") as fr:
    #     aoyama_contents = json.load(fr)
    # aoyama_payment_sum = calc_payment_sum(aoyama_contents, "aoyama")
    
    # with open("json/mizuhobank_balance.json", "r") as fr:
    #     mizuhobank_balance_sum = json.load(fr)
    
    
    return render_template(
        "index.html", 
        title="please money", 
        views=views_payment_sum, 
        rakuten=rakuten_payment_sum,
        epos=epos_payment_sum,
        aoyama=aoyama_payment_sum,
        bank=mizuhobank_balance_sum,
        bonus=views_bonus_value
        )


# @app.route("/scraping")
# def scraping():
#     # スクレイピングにより各変数を更新
#     views_thread = threading.Thread(target=views_scraping_func)
#     views_thread.start()
    
#     rakuten_thread = threading.Thread(target=rakuten_scraping_func)
#     rakuten_thread.start()
    
#     aoyama_thread = threading.Thread(target=aoyama_scraping_func)
#     aoyama_thread.start()
    
#     epos_thread = threading.Thread(target=epos_scraping_func)
#     epos_thread.start()
    
#     mizuhobank_thread = threading.Thread(target=mizuhobank_scraping_func)
#     mizuhobank_thread.start()


#     return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)