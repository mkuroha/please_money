def calc_payment_sum(contents, card_company):
    """
    contents: list [利用日，支払先，金額，何回払い]]
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


def separate_payment(value, count, card_company):
    """
    value: int 
    count: int
    card_company: str
    """
    separate_value = value
    if card_company=="views":
        return separate_value
    elif card_company=="rakuten":
        fee_dict = {3:2.04, 5:3.4, 6:4.08, 10:6.8, 12:8.16, 15:10.2, 18:12.24, 20:13.6, 24:16.32, 30:20.4, 36:24.48}
        all_fee = value // 100 * fee_dict[count]
        separate_value = int( (value+all_fee) / count )
        return separate_value
    elif card_company=="aoyama":
        fee_dict = {3:2.04, 5:3.4, 6:4.08, 10:6.8, 12:8.16, 15:10.2, 18:12.24, 20:13.6, 24:16.32}
        all_fee = value // 100 * fee_dict[count]
        separate_value = int( (value+all_fee) / count )
        return separate_value
    elif card_company=="epos":
        return separate_value
    
if __name__ == "__main__":
    calc_()