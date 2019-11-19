import time
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# 定数宣言
REPEAT_NUM = 5  # セレニウムの起動 繰り返し回数
CHROME_VERSION = "78"  # Chromeのバージョン管理


def views_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    with open("json/login_info.json", "r") as fr:
        login_info = json.load(fr)
    
    login_url = "https://viewsnet.jp/default.htm#_ga=2.25949684.897350575.1567924740-403201021.1550140754"
    
    html = None
    num = 0
    output_html_list = []
    while(html is None):
        num += 1
        if num>REPEAT_NUM:
            break
        
        try:
            # headless version
            driver = webdriver.Chrome(executable_path='./chromedriver/{}/chromedriver.exe'.format(CHROME_VERSION), options=options)
            
            # ログイン
            driver.get(login_url)
            id = driver.find_element_by_xpath('//*[@id="id"]')
            id.send_keys(login_info["views"]["id"])
            time.sleep(1)
            password = driver.find_element_by_xpath('//*[@id="pass"]')
            password.send_keys(login_info["views"]["pass"])
            time.sleep(2)
            login_button = driver.find_element_by_xpath('//*[@id="input_form"]/form/p/input')
            login_button.click()
            time.sleep(2)
            
            # ご利用明細画面
            time.sleep(2)
            details_button = driver.find_element_by_xpath('//*[@id="LnkV0300_001Top"]/img')
            details_button.click()
            time.sleep(2)
            
            # 請求予定の明細画面
            yotei_button = driver.find_element_by_xpath('//*[@id="LnkYotei"]')
            yotei_button.click()
            time.sleep(2)
            
            # このページをスクレイピングする
            html = driver.page_source
            output_html_list.append(html)
            
            # 次へボタンがあるかどうかを確認
            time.sleep(4)
            try:
                next_button = driver.find_element_by_xpath('//*[@id="LnkNextBottom"]')
                next_button.click()
                time.sleep(4)
                html2 = driver.page_source
                output_html_list.append(html2)
                
            except:
                pass
            
            driver.quit()
            
        except:
            driver.quit()
            continue

    # 終了
    driver.quit()
    
    # with open("views.html", "w", encoding="utf-8") as fw:
    #     fw.write(output_html_list[0])
    
    return output_html_list

    

def rakuten_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    with open("json/login_info.json", "r") as fr:
        login_info = json.load(fr)
    login_url = "https://www.rakuten-card.co.jp/e-navi/index.xhtml"
    
    html = None
    num = 0
    output_html_list = []
    while(html is None):
        num += 1
        if num>REPEAT_NUM:
            break
        
        try:
            # headless version
            driver = webdriver.Chrome(executable_path='./chromedriver/{}/chromedriver.exe'.format(CHROME_VERSION), options=options)
            
            # ログイン
            driver.get(login_url)
            time.sleep(3)
            radiobutton = driver.find_element_by_xpath('//*[@id="loginChk"]/div/label')
            radiobutton.click()
            id = driver.find_element_by_xpath('//*[@id="u"]')
            time.sleep(1)
            id.send_keys(login_info["rakuten"]["id"])
            time.sleep(2)
            password = driver.find_element_by_xpath('//*[@id="p"]')
            time.sleep(1)
            password.send_keys(login_info["rakuten"]["pass"])
            time.sleep(2)
            login_button = driver.find_element_by_id("loginSbm")
            login_button.click()
            time.sleep(4)
            
            # ご利用明細画面
            details_button = driver.find_element_by_xpath('//*[@id="js-prefix-title"]/div/a')
            time.sleep(3)
            details_button.click()
            time.sleep(4)
            
            # 請求予定の明細画面
            try:
                yotei_button = driver.find_element_by_xpath('//*[@id="contentsArea_statement"]/div[2]/div[2]/div[1]/div[1]/a[2]')
                yotei_button.click()
                time.sleep(2)
                html = driver.page_source
                output_html_list.append(html)
            except:
                time.sleep(4)
                html = driver.page_source
                output_html_list.append(html)
            
        except:
            driver.quit()
            continue
            
        # 終了
        driver.quit()
    
    driver.quit()
    
    # with open("rakuten.html", "w", encoding="utf-8") as fw:
    #     fw.write(output_html_list[0])
    
    return output_html_list


def mizuhobank_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    with open("json/login_info.json", "r") as fr:
        login_info = json.load(fr)
    login_url = "https://web.ib.mizuhobank.co.jp/servlet2/CASBNK60000B.do"
    
    html = None
    num = 0
    while(html is None):
        num += 1
        if num>REPEAT_NUM:
            break
        try:
            # headless version
            driver = webdriver.Chrome(executable_path='./chromedriver/{}/chromedriver.exe'.format(CHROME_VERSION), options=options)            
            
            # ログイン
            driver.get(login_url)
            time.sleep(4)
            shopno = driver.find_element_by_xpath('//*[@id="txbBrnchNo"]')
            time.sleep(1)
            shopno.send_keys(login_info["mizuhobank"]["shopno"])
            time.sleep(1)
            trans_type = driver.find_element_by_xpath('//*[@id="main-nomenu"]/article/table/tbody/tr[2]/td/ul/li[1]/div[2]/label')
            time.sleep(1)
            trans_type.click()
            accountno = driver.find_element_by_xpath('//*[@id="txbAccNo"]')
            time.sleep(1)
            accountno.send_keys(login_info["mizuhobank"]["accountno"])
            time.sleep(1)
            password = driver.find_element_by_xpath('//*[@id="PASSWD_LoginPwd"]')
            time.sleep(1)
            password.send_keys(login_info["mizuhobank"]["pass"])
            time.sleep(4)
            
            login_button = driver.find_element_by_xpath('//*[@id="main-nomenu"]/section[1]/article/input')
            login_button.click()
            time.sleep(4)
            
            # このページをスクレイピング
            html = driver.page_source
        
        except:
            # import traceback
            # traceback.print_exc()
            
            driver.quit()
            continue
    
    # 終了
    driver.quit()
    
    # with open("mizuhobank.html", "w", encoding="utf-8") as fw:
    #     fw.write(html)
    
    return html
    

def aoyama_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    with open("json/login_info.json", "r") as fr:
        login_info = json.load(fr)
    login_url = "https://www3.lifecard.co.jp/WebDesk/www/login.html"
    
    html = None
    num = 0
    while(html is None):
        num += 1
        if num>REPEAT_NUM:
            break
        try:
            # headless version
            driver = webdriver.Chrome(executable_path='./chromedriver/{}/chromedriver.exe'.format(CHROME_VERSION), options=options)
            
            # ログイン
            driver.get(login_url)
            time.sleep(4)
            id = driver.find_element_by_xpath('//*[@id="webmbrId"]')
            time.sleep(1)
            id.send_keys(login_info["aoyama"]["id"])
            time.sleep(2)
            password = driver.find_element_by_xpath('//*[@id="webmbrPasswd"]')
            time.sleep(1)
            password.send_keys(login_info["aoyama"]["pass"])
            time.sleep(4)
            
            login_button = driver.find_element_by_xpath('//*[@id="doLogin"]')
            login_button.click()
            
            # 追加認証
            time.sleep(4)
            first = driver.find_element_by_xpath('//*[@id="addAuthForm"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[1]/div[1]').text
            second = driver.find_element_by_xpath('//*[@id="addAuthForm"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[1]/div[5]').text
            
            if first[1]=="文":
                first_str = login_info["aoyama"]["name"][int(first[0])-1]
            else:
                first_str = login_info["aoyama"]["name"][int(first[:2])-1]
            
            if second[1]=="文":
                second_str = login_info["aoyama"]["name"][int(second[0])-1]
            else:
                second_str = login_info["aoyama"]["name"][int(second[:2])-1]
            
            id1 = driver.find_element_by_xpath('//*[@id="firstString"]')
            time.sleep(1)
            id1.send_keys(first_str)
            
            id2 = driver.find_element_by_xpath('//*[@id="secondString"]')
            time.sleep(1)
            id2.send_keys(second_str)
            time.sleep(1)
            login_button = driver.find_element_by_xpath('//*[@id="doAddAuth"]')
            login_button.click()

            
            # ご利用明細画面
            time.sleep(2)
            details_button = driver.find_element_by_xpath('//*[@id="goSeikySel1-2"]/img')
            details_button.click()
            time.sleep(4)

            
            # 請求予定の明細画面
            yotei_button = driver.find_element_by_xpath('//*[@id="goSeikyVie8"]/img')
            yotei_button.click()
            time.sleep(4)
            
            # このページをスクレイピング
            html = driver.page_source
        except:
            # import traceback
            # traceback.print_exc()
            
            driver.quit()
            continue
    
    # with open("aoyama.html", "w", encoding="utf-8") as fw:
    #     fw.write(html)
    
    # 終了
    driver.quit()
    

    return html
    

def epos_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    with open("json/login_info.json", "r") as fr:
        login_info = json.load(fr)
    login_url = "https://www.eposcard.co.jp/memberservice/pc/login/login_preload.do"
    
    html = None
    num = 0
    while(html is None):
        num += 1
        if num>REPEAT_NUM:
            break
        try:
            # headless version
            driver = webdriver.Chrome(executable_path='./chromedriver/{}/chromedriver.exe'.format(CHROME_VERSION), options=options)
            
            # ログイン
            driver.get(login_url)
            time.sleep(3)
            id = driver.find_element_by_xpath('//*[@id="mainContents"]/div/div[1]/form/div[1]/div[2]/input')
            id.send_keys(login_info["epos"]["id"])
            time.sleep(2)
            password = driver.find_element_by_xpath('//*[@id="mainContents"]/div/div[1]/form/div[2]/div[2]/input')
            password.send_keys(login_info["epos"]["pass"])
            time.sleep(2)
            # お支払予定額を見る
            login_button = driver.find_element_by_xpath('//*[@id="mainContents"]/div/div[1]/form/p/a')
            login_button.click()
            
            # ご利用明細画面
            time.sleep(2)
            details_button = driver.find_element_by_xpath('//*[@id="naviBlock"]/div/div[1]/div[1]/p[2]/a')
            details_button.click()
            time.sleep(4)
            
            # 請求予定の明細画面 次回お支払い分のご利用詳細はこちら
            yotei_button = driver.find_element_by_xpath('//*[@id="mainContents"]/div/form/div[3]/table/tbody/tr[4]/td[2]/p[1]/input')
            yotei_button.click()
            time.sleep(4)
            
            # このページをスクレイピング
            html = driver.page_source
        except:
            import traceback
            traceback.print_exc()
            
            driver.quit()
            continue
    
    # with open("epos.html", "w", encoding="utf-8") as fw:
    #     fw.write(html)
    
    # 終了
    driver.quit()
    
    return html
    
    
if __name__ == "__main__":
    pass
    # print("views")
    # views_selenium()
    # print("rakuten")
    # rakuten_selenium()
    # print("mizuho")
    # mizuhobank_selenium()
    # print("aoyama")
    # aoyama_selenium()
    # print("epos")
    # epos_selenium()
    