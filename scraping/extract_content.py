import time
import re
import copy
from datetime import datetime as dt
import datetime
import psycopg2

from bs4 import BeautifulSoup


"""
各クレジットカード会社のHTMLを受け取り，そこから利用明細をリストとして取得
リストの中
[使用日(datetime)，クレジットカード会社名(str)，使用金額(int)，使用用途(str)，支払方法(str, 1, 2, 12, ボ) ]
支払日は，各会社で使用日から算出してリストに追加する
"""

def calc_payment_date(tmp_list):
    """
    カード会社ごとに支払日の計算をする関数
    
    Paramters
    ---------
    tmp_list: list型 [使用日（datetime），カード会社（str），金額（int），使用用途（str），支払方法（str, "1", "2", ...）]
    
    Output
    ------
    output: list型
    
    """
    output = copy.deepcopy(tmp_list)
    tdate = output[0]
    card_company = output[1]
    payment_method = output[5]
    
    
    if card_company=="Views":
        return output
        
    elif card_company=="Rakuten":
        return output
        
    elif card_company=="EPOS":
        return output
        
    elif card_company=="Aoyama":
        return output
        
    
    else:
        return output
    

def is_exists(cur, time, company_name, cost):
    # データベースにtime, costのものがあるかをTrue or Falseで返す関数
    # ある場合Trueになる
    cur.execute(
        "SELECT EXISTS (SELECT * FROM %s WHERE time=%s AND company_name=%s AND cost=%s )", (database, time, company_name, cost) 
        )
    tmp = cur.fetchone()
    # print(tmp)
    
    return tmp[0]


def is_exists_for_bank(cur, date, value, content):
    # データベースにtime, costのものがあるかをTrue or Falseで返す関数
    # ある場合Trueになる
    cur.execute(
        "SELECT EXISTS (SELECT * FROM bank WHERE date=%s AND value=%s AND usage=%s )", (date, value, content) 
        )
    tmp = cur.fetchone()
    
    
    return tmp[0]


# 取得したHTMLから欲しい情報を取得し，データベースに保存する関数
def views_scraping(views_html):
    # データベース接続
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    
    try:
        for html in views_html:
            soup = BeautifulSoup(html, "html.parser")
            rows = soup.find_all("tr")  # 3個目以降が支出
            
            for i, row in enumerate(rows[3:]):
                output_tmp = [None, None, None, None, None]
                details = row.find_all("span")
                
                year = details[0].text  # 2019
                date = details[1].text  # 07/17
                tmp_date = year+"/"+date
                tdatetime = dt.strptime(tmp_date, '%Y/%m/%d')
                output_tmp[0] = tdatetime
                
                output_tmp[1] = "Views"  # カード会社名
                
                value = details[3].text  # 12,000
                value = int( value.replace(",", "") )  # 31,920の,を除く
                output_tmp[2] = value
                
                payment = row.find_all("strong")[0].text.replace('\u3000', ' ')
                output_tmp[3] = payment
                
                output_type = details[-1].text  # ショッピングボーナス一括払い or ショッピング１回払い
                if output_type=="ショッピング１回払い":
                    output_tmp[4] = "1"
                elif output_type=="ショッピングボーナス一括払い":
                    output_tmp[4] = "ボ"
                elif output_type=="ショッピング２回払い":
                    output_type[4] = "2"
                else:
                    pass
                
                if is_exists(cur=cur, time=output_tmp[0], company_name=output_tmp[1], cost=output_tmp[2]):
                    pass
                    print('a')
                else:  # データベース内にデータがない場合
                    # データベースに保存
                    print("b")
                    cur.execute(
                        "INSERT INTO payment (time, company_name, cost, usage, payment_type) VALUES (%s, %s, %s, %s, %s)", (output_tmp[0], output_tmp[1], output_tmp[2], output_tmp[3], output_tmp[4])
                        )
        conn.commit()
        
    except:
        print("No data")
    
    cur.close()
    conn.close()


def mizuhobank_scraping(mizuhobank_html):
    """
    Input
    ------
    mizuhobank_html: みずほ銀行インターネットかんたん残高照会のHTML
    
    Output
    ------
    
    """
    # データベース接続
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    
    output = []
    soup = BeautifulSoup(mizuhobank_html, "html.parser")
    tables = soup.find_all("table", class_="n61000-t3")
    tables = tables[0].find_all("tr")
    
    for i, table in enumerate(tables):
        
        if i==0:
            pass
        else:
            details = table.find_all("td")
            # print(details)
            
            # 日付
            date = details[0].text
            tdate = dt.strptime(date, '%Y.%m.%d')

            # 引出金額
            value_minus = details[1].text
            # 預入金額
            value_plus = details[2].text
            
            try:
                value = - int( value_minus.replace("\xa0", "").replace("円", "").replace(",", "") )
            except:
                value = int( value_plus.replace("\xa0", "").replace("円", "").replace(",", "") )
            
            # 取引内容
            content = details[3].text
            content = content.replace("\u3000", "")
            
            
            # データベースへの格納方法
            if is_exists_for_bank(cur=cur, date=date, value=value, content=content):
                pass
            else:  # データベース内にデータがない場合
                # データベースに保存
                cur.execute(
                    "INSERT INTO bank (date, value, usage) VALUES (%s, %s, %s)", (date, value, content)
                    )
    
    conn.commit()
    cur.close()
    conn.close()


def rakuten_scraping(rakuten_html):
    # データベース接続
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    
    try:
        for html in rakuten_html:
            soup = BeautifulSoup(html, "html.parser")
            tmp = soup.find_all('div', class_="stmt-payment-lists__i js-payment-accordion-ctrl is-close js-payment-sort-item")
            
            for i, row in enumerate(tmp):
                output_tmp = [None, None, None, None, None]
                
                details = row.find_all("div", class_="stmt-payment-lists__data")
                
                # 利用日
                date = details[0].text  # 2019/09/28
                date = date.replace('\n', '').replace(" ", "")
                tdate = dt.strptime(date, '%Y/%m/%d')
                output_tmp[0] = tdate
                
                # カード会社
                output_tmp[1] = "Rakuten"
                
                # 金額
                value = details[4].text  # ￥ 1,030
                value = int( value.replace("¥", "").replace(" ", "").replace("\n", "").replace(",", "") )  # ¥などを消す
                output_tmp[2] = value
                
                # 利用用途
                payment = details[1].text
                payment = payment.replace('\u3000', '').replace("\n", "").replace(" ", "")
                for moji in payment:
                    if re.match("\d", moji):
                        payment = payment.replace(moji, "")
                output_tmp[3] = payment
                
                # 支払方法
                output_type = details[3].text  # ショッピングボーナス一括払い or ショッピング１回払い
                output_type = output_type.replace('\n', '').replace(" ", "")
                output_tmp[4] = output_type.split("回")[0]
                
                if is_exists(cur=cur, time=output_tmp[0], company_name=output_tmp[1], cost=output_tmp[2]):
                    pass
                else:  # データベース内にデータがない場合
                    # データベースに保存
                    cur.execute(
                        "INSERT INTO payment (time, company_name, cost, usage, payment_type) VALUES (%s, %s, %s, %s, %s)", (output_tmp[0], output_tmp[1], output_tmp[2], output_tmp[3], output_tmp[4])
                        )
        conn.commit()
        
    except:
        print("No data")
    
    cur.close()
    conn.close()
    

def epos_scraping(epos_html):
    """
    
    Output
    ------
    """
    print("epos_scraping")
    
    # データベース接続
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    
    soup = BeautifulSoup(epos_html, "html.parser")
    rows = soup.find_all("td", class_="checkCell")
    try:
        output_tmp = [None, None, None, None, None]
        for i, row in enumerate(rows):
            detail = row.text
            
            if i%5==0:  # ご利用年月日
                # detail = datetime(detail)
                detail = detail.replace("\n", "").replace(" ", "")
                tdatetime = dt.strptime(detail, '%Y/%m/%d')
                output_tmp[0] = tdatetime
            elif i%5==1:  # ご利用場所
                output_tmp[3] = detail
            elif i%5==2:  # ご利用内容（なぜか空欄）
                pass
            elif i%5==3:  # ご利用金額
                detail = int( detail.replace('\u3000', '').replace("\n", "").replace(" ", "").replace("円", "").replace(",", "") )
                output_tmp[2] = detail
            else:  # 備考
                output_tmp[1] = "EPOS"
                output_tmp[4] = "1"
                
                # DB格納
                if is_exists(cur=cur, time=output_tmp[0], company_name=output_tmp[1], cost=output_tmp[2]):
                    pass
                else:  # データベース内にデータがない場合
                    # データベースに保存
                    cur.execute(
                        "INSERT INTO payment (time, company_name, cost, usage, payment_type) VALUES (%s, %s, %s, %s, %s)", (output_tmp[0], output_tmp[1], output_tmp[2], output_tmp[3], output_tmp[4])
                        )       
        conn.commit()
        
    except:
        print("No data")
    
    cur.close()
    conn.close()


def aoyama_scraping(aoyama_html):
    """
    Input
    ------
    aoyama_html
    
    
    Output
    ------
    
    """
    # データベース接続
    conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    cur = conn.cursor()
    
    soup = BeautifulSoup(aoyama_html, "html.parser")
    try:
        dates = soup.find_all("span", id="riyoYmd")  # 利用日 2019/09/17
        payments = soup.find_all("span", id="kmmei")  # 支払先
        values = soup.find_all("span", id="kagKin")  # 金額
        output_type = soup.find_all("span", id="num")  # 支払い方法
        
        output = []
        for tmp_tuple in zip(dates, payments, values, output_type):
            output_tmp = [None, None, None, None, None, None]
            
            # 利用日
            date = tmp_tuple[0].text
            tdate = dt.strptime(date, '%Y/%m/%d')
            output_tmp[0] = tdate
            
            # カード会社
            output_tmp[1] = "Aoyama"
            
            # 金額
            value = tmp_tuple[2].text
            value = int( value.replace(",", "") )
            output_tmp[2] = value
            
            # 使用用途
            payment = tmp_tuple[1].text
            payment = payment.replace("\u3000", "")
            output_tmp[3] = payment
            
            output_type = tmp_tuple[3].text # "12"
            output_tmp[4] = output_type
            
            # DB格納
            if is_exists(cur=cur, time=output_tmp[0], company_name=output_tmp[1], cost=output_tmp[2]):
                pass
            else:  # データベース内にデータがない場合
                # データベースに保存
                cur.execute(
                    "INSERT INTO payment (time, company_name, cost, usage, payment_type) VALUES (%s, %s, %s, %s, %s)", (output_tmp[0], output_tmp[1], output_tmp[2], output_tmp[3], output_tmp[4])
                        )
        conn.commit()
    
    except:
        print("No data")
    
    cur.close()
    conn.close()


if __name__ == "__main__":
    pass
    
    # データベースチェック
    # with open("aoyama.html", "r", encoding="utf-8") as fr:
    #     views_html = fr.read()
    # aoyama_scraping(views_html)
    
    # conn = psycopg2.connect("dbname=please_money host=localhost user=postgres password=kurochan0917")
    # cur = conn.cursor()
    
    # # cur.execute("truncate bank;") # 初期化（テーブルは残す）
    # # cur.execute("DROP TABLE bank;")  # テーブルを削除
    
    # # cur.execute("CREATE TABLE bank (id serial PRIMARY KEY, date timestamp, value integer, usage varchar)")
    # # cur.execute("CREATE TABLE payment (id serial PRIMARY KEY, time timestamp, company_name varchar, cost integer, usage varchar, payment_type varchar)")
    
    # # for tag, info in student_dict.items():
    # #     cur.execute("INSERT INTO takeda_database (tag, name, subject) VALUES (%s, %s, %s)", (tag, info["name"], info["subject"]))
    
    # # cur.execute("SELECT * FROM payment;")
    # # test = cur.fetchall()
    # conn.commit()
    
    # cur.close()
    # conn.close()
    
    # with open("mizuhobank.html", "r", encoding="utf-8") as fr:
    #     mizuho_html = fr.read()
    # mizuhobank_scraping(mizuho_html)