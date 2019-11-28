import json
import datetime
import copy
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

START_BANK_BALANCE = 28673
# 84076

def calc_bank_balance(alldata):
    """
    データベースの情報を受け取って口座残高を算出して返す
    
    Output
    ------
    bank_balance: int型
    
    """
    bank_balance = START_BANK_BALANCE
    
    for data in alldata:
        
        value = data[2]
        bank_balance += value
    
    return bank_balance


def conversion_holiday_to_weekday(tdate):
    """
    入力されたdatetimeが土日である場合に平日に変換する関数
    """
    if tdate.weekday() > 4:
        tdate = tdate + datetime.timedelta(days=4-tdate.weekday())
    
    return tdate


def conversion_day_to_four(tdate):
    if tdate.day<4:
        tdate = tdate + datetime.timedelta(days=4-tdate.day)
    
    return tdate


def calc_payment_date(usedate, card_company, payment_type):
    """
    カード会社ごとに，利用日と支払方法から支払日を算出する関数?
    
    usedate: datetime型
    card_company: str型
    payment_type: str型
    
    
    """
    year = usedate.year
    month = usedate.month
    day = usedate.day
    now = dt.now()
    
    # 定数宣言，各カード会社の締め日と支払日
    VIEWS_PAYMENT_DATE = 4
    RAKUTEN_PAYMENT_DATE = 27
    AOYAMA_CLOSING_DATE = 5
    AOYAMA_PAYMENT_DATE = 3
    EPOS_CLOSING_DATE = 4
    EPOS_PAYMENT_DATE = 4
    
    # Viewsカード
    if card_company=="Views":
        if month==11: # 12月の分                
            # 支払日が土日のとき平日に変換
            next_payment_day = conversion_holiday_to_weekday(dt(year+1, 1, VIEWS_PAYMENT_DATE))
        elif month==12:
            next_payment_day = conversion_holiday_to_weekday(dt(year+1, 2, VIEWS_PAYMENT_DATE))
        else:
            next_payment_day = conversion_holiday_to_weekday(dt(year, month+2, VIEWS_PAYMENT_DATE))
        
        if payment_type=="1":
            return next_payment_day
        
        elif payment_type=="ボ":  # ボーナス一括払い
            if month<7:
                return conversion_holiday_to_weekday(dt(year, 8, VIEWS_PAYMENT_DATE))  # 8月
            else:
                return conversion_holiday_to_weekday(dt(year+1, 1, VIEWS_PAYMENT_DATE))  # 1月
        else:  # 2, 3,..., 12回払い 
            for i in range(int(payment_type)):
                next_payment_day = next_payment_day + relativedelta(months=1)
                if (now - next_payment_day).days<-1 and (now - next_payment_day).days>-30 :
                    return conversion_holiday_to_weekday(conversion_day_to_four(next_payment_day))
            
            # なかった場合，最後の日にちを返す
            return conversion_holiday_to_weekday(conversion_day_to_four(next_payment_day))
    
    # 楽天カード
    elif card_company=="Rakuten":
        if month==12: 
            next_payment_day = conversion_holiday_to_weekday(dt(year+1, 1, RAKUTEN_PAYMENT_DATE))
        else: 
            next_payment_day = conversion_holiday_to_weekday(dt(year, month+1, RAKUTEN_PAYMENT_DATE))
        if payment_type=="1":  # 一回払い
            return next_payment_day
        else:  # 分割払い
            for i in range(int(payment_type)):
                next_payment_day = next_payment_day + relativedelta(months=1)
                if (now - next_payment_day).days<-1 and (now - next_payment_day).days>-30 :
                    return conversion_holiday_to_weekday(conversion_day_to_four(next_payment_day))
            
            # なかった場合，最後の日にちを返す
            return conversion_holiday_to_weekday(conversion_day_to_four(next_payment_day))
    
    # 青山カード
    elif card_company=="Aoyama":
        if day<=AOYAMA_CLOSING_DATE:  # 1-5日のとき
            if month==12:
                next_payment_day = conversion_holiday_to_weekday(dt(year+1, 1, AOYAMA_PAYMENT_DATE))
            else:
                next_payment_day = conversion_holiday_to_weekday(dt(year, month+1, AOYAMA_PAYMENT_DATE))
        else: # 6日以降のとき
            if month==11:
                next_payment_day = conversion_holiday_to_weekday(dt(year+1, 1, AOYAMA_PAYMENT_DATE))
            elif month==12:
                next_payment_day = conversion_holiday_to_weekday(dt(year+1, 2, AOYAMA_PAYMENT_DATE))
            else:
                next_payment_day = conversion_holiday_to_weekday(dt(year, month+2, AOYAMA_PAYMENT_DATE))
        
        if payment_type=="1":  # 1回払い
            return next_payment_day
        else:  # 分割払い
            for i in range(int(payment_type)):
                next_payment_day = next_payment_day + relativedelta(months=1)
                if (now - next_payment_day).days<-1 and (now - next_payment_day).days>-30 :
                    return conversion_holiday_to_weekday(conversion_day_to_four(next_payment_day))
            
            # なかった場合，最後の日にちを返す
            return conversion_holiday_to_weekday(conversion_day_to_four(next_payment_day))
    
    # エポスカード
    elif card_company=="EPOS":
        if day<=EPOS_CLOSING_DATE:  # 1-4日のとき
            if month==12:
                next_payment_day = conversion_holiday_to_weekday(dt(year+1, 1, EPOS_PAYMENT_DATE))
            else:
                next_payment_day = conversion_holiday_to_weekday(dt(year, month+1, EPOS_PAYMENT_DATE))
        else: # 5日以降のとき
            if month==11:
                next_payment_day = conversion_holiday_to_weekday(dt(year+1, 1, EPOS_PAYMENT_DATE))
            elif month==12:
                next_payment_day = conversion_holiday_to_weekday(dt(year+1, 2, EPOS_PAYMENT_DATE))
            else:
                next_payment_day = conversion_holiday_to_weekday(dt(year, month+2, EPOS_PAYMENT_DATE))
        if payment_type=="1":  # 1回払い
            return next_payment_day
        else:  # 分割払い
            for i in range(int(payment_type)):
                next_payment_day = next_payment_day + relativedelta(months=1)
                if (now - next_payment_day).days<-1 and (now - next_payment_day).days>-30 :
                    return conversion_holiday_to_weekday(conversion_day_to_four(next_payment_day))
            
            # なかった場合，最後の日にちを返す
            return conversion_holiday_to_weekday(conversion_day_to_four(next_payment_day))


def extract_close_payment(alldata):
    """
    データの分割払い計算，支払日計算してリストで返す
    
    Input
    -----
    data: list型
          [[使用日(datetime)，クレジットカード会社名(str)，使用金額(int)，使用用途(str)，支払方法(str, 1, 2, 12, ボ) ], ]
    
    Output
    ------
    alloutput: list 全ての支払い情報（過去，未来含む）を含むリスト
    nearoutput: list 直近の支払い情報のみを含むリスト
    
    """
    alldata = copy.deepcopy(alldata)
    alloutput = []  # 全てのデータ
    near_output = []  # 支払日が先にあるもののみを格納
    for eachdata in alldata:
        use_date = eachdata[1]
        card_company = eachdata[2]
        value = eachdata[3]
        payment_type = eachdata[5]
        output = [use_date, card_company, None, eachdata[4], payment_type]
        
        # 分割払い算出
        if payment_type=="1" or payment_type=="ボ":  # 
            output[2] = value
        else:  # 分割払いの場合
            separated_value = separate_payment(value=value, payment_type=int(payment_type), card_company=card_company)
            output[2] = separated_value
        
        # 支払日の算出
        payment_date = calc_payment_date(usedate=use_date, card_company=card_company, payment_type=payment_type)
        output.append(payment_date)
        
        alloutput.append(output)
        
        # 支払日が現在よりも先にあるデータのみ取り出す
        now_time = dt.now()
        if (now_time - payment_date).days < 0:
            near_output.append(output)        
    
    return alloutput, near_output


def calc_payment_sum(contents, card_company):
    """
    contents: list [[利用日，支払先，金額，何回払い]]
    type: str  views, rakuten, aoyama, epos
    """
    payment_sum = 0
    bonus_value = 0
    for tmp in contents:
        value = int(tmp[2])
        payment_type = str(tmp[3])
        
        if payment_type=="1回払" or payment_type=="1" or payment_type=="1回払い" or payment_type=="ショッピング１回払い":
            payment_sum += value
        elif payment_type=="ショッピングボーナス一括払い":  # viewsのときのみ
            bonus_value += value
        
        # 分割払いの計算
        else:
            # TODO: 要検討，1回払い，1回払，1, 12，など複数あり
            tmp_len = len(payment_type)
            if tmp_len==1 or tmp_len==2:
                payment_type = int(payment_type)
            elif tmp_len==3:
                payment_type = int(payment_type[0])
            
            # paymentをint型に変換後，計算
            separate_value = separate_payment(value, payment_type, card_company)
            payment_sum += separate_value
    
    # 合計を返す
    if card_company=="views":
        return payment_sum, bonus_value
    else:
        return payment_sum


def separate_payment(value, payment_type, card_company):
    """
    value: int 
    payment_type: int
    card_company: str
    """
    separate_value = value
    fee_dict = {3:2.04, 5:3.4, 6:4.08, 10:6.8, 12:8.16, 15:10.2, 18:12.24, 20:13.6, 24:16.32, 30:20.4, 36:24.48}
    
    if card_company=="Views":
        return separate_value
    elif card_company=="Rakuten":
        all_fee = value // 100 * fee_dict[payment_type]
        separate_value = int( (value+all_fee) / payment_type )
        return separate_value
    elif card_company=="Aoyama":
        all_fee = value // 100 * fee_dict[payment_type]
        separate_value = int( (value+all_fee) / payment_type )
        return separate_value
    else:
        pass


if __name__ == "__main__":
    pass