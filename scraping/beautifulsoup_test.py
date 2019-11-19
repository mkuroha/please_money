import time
import re

from bs4 import BeautifulSoup
from pprint import pprint


def views_test():
    with open("views_html.html", encoding="utf-8") as fr:
        html = fr.read()
    
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")  # 3個目以降が支出
    # print("rows: ", rows)
    
    output = []
    
    for i, row in enumerate(rows[3:]):
        # time.sleep(1)
        
        # print("###############################")
        if i==0:
            pass
            # print(row)  # rowの例が下にある
        
        payment = row.find_all("strong")[0].text.replace('\u3000', ' ')
        
        details = row.find_all("span")
        # print("details: ", detaails)
        
        year = details[0].text  # 2019
        # print("year: ", year)
        
        date = details[1].text  # 07/17
        # print("date: ", date)
        
        value = details[3].text  # 12,000
        # print("value: ", value)
        
        # 31,920の,を除く
        value = int( value.replace(",", "") )
        
        output_type = details[-1].text  # ショッピングボーナス一括払い or ショッピング１回払い
        # print("output type: ", output_type)
        
        output.append( [year+"/"/date, payment, value, output_type] )
        
        # データ整形，格納
        # すでにデータベースにある場合はcontinue
    
    # 次へボタンがあるかの判断，あったらページ遷移してから上と同じことを繰り返す
    # if 
    # //*[@id="LnkNextBottom"]
    pprint(output)


def aoyama_test():
    with open("aoyama_html.html", encoding="utf-8") as fr:
        html = fr.read()
    
    soup = BeautifulSoup(html, "html.parser")
    dates = soup.find_all("span", id="riyoYmd")  # 利用日
    payments = soup.find_all("span", id="kmmei")  # 支払先
    values = soup.find_all("span", id="kagKin")  # 金額
    output_type = soup.find_all("span", id="num")  # 支払い方法
    
    output = []
    for tmp_tuple in zip(dates, payments, values, output_type):
        date = tmp_tuple[0].text
        payment = tmp_tuple[1].text
        payment = payment.replace("\u3000", "")

        value = tmp_tuple[2].text
        value = int( value.replace(",", "") )
        
        output_type = tmp_tuple[3].text
        
        output.append([date, payment, value, output_type])
        
    return output



def rakuten_test():
    with open("rakuten_html.html", encoding="utf-8") as fr:
        html = fr.read()
    
    soup = BeautifulSoup(html, "html.parser")
    tmp = soup.find_all('div', class_="stmt-payment-lists__i js-payment-accordion-ctrl is-close js-payment-sort-item")
    
    output = []
    for i, row in enumerate(tmp):
        time.sleep(1)
        details = row.find_all("div", class_="stmt-payment-lists__data")
        
        date = details[0].text  # 2019/09/28
        date = date.replace('\n', '').replace(" ", "")
        
        payment = details[1].text
        payment = payment.replace('\u3000', '').replace("\n", "").replace(" ", "")
        for moji in payment:
            if re.match("\d", moji):
                payment = payment.replace(moji, "")
        
        output_type = details[3].text  # ショッピングボーナス一括払い or ショッピング１回払い
        output_type = output_type.replace('\n', '').replace(" ", "")
        
        value = details[4].text  # ￥ 1,030
        value = int( value.replace("¥", "").replace(" ", "").replace("\n", "").replace(",", "") )  # ¥などを消す
        # print(value)
        
        output.append( [date, payment, value, output_type] )
    
    output.sort()
    # pprint(output)
    
    return output


def mizuhobank_test():
    """
    Output
    ------
    bank balance: 口座残高（int）
    ------
    """
    with open("mizuhobank_html.html", encoding="utf-8") as fr:
        html = fr.read()
    
    output = []
    soup = BeautifulSoup(html, "html.parser")
    tmp = soup.find('table', class_="n61000-t2")
    rows = tmp.find_all("tr")
    
    content = rows[4]
    bank_balance = content.find("span").text  # 109,447 円
    bank_balance = int( bank_balance.replace("\xa0", "").replace("円", "").replace(",", "") )
    
    return bank_balance



def epos_test():
    with open("epos_html.html", encoding="utf-8") as fr:
        html = fr.read()
    
    soup = BeautifulSoup(html, "html.parser")
    
    date_near = soup.find("p", class_="refDate-cr").text  # 支払日 2019年10月4日
    date_near = date_near.replace("年", "/").replace("月", "/").replace("日", "").replace(" ", "").replace("\n", "")
    
    date_next = soup.find("p", class_="refDate-next").text
    date_next = date_next.replace("年", "/").replace("月", "/").replace("日", "").replace(" ", "").replace("\n", "")
    
    near_values = soup.find_all("p", class_="refPayment-cr")[0]  # 金額
    near_values = int( near_values.find_all("span")[0].text )
    
    next_values = soup.find_all("p", class_="refPayment-next")[0]  # 金額
    next_values = int( next_values.find_all("span")[0].text )
    
    return [date_near, near_values, date_next, next_values]


if __name__ == "__main__":
    pass
    # views_test()
    # aoyama_test()
    # rakuten_test()
    # mizuhobank_test()
    # epos_test()