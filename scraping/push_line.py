import requests


def push_line():
    """
    LINE通知用関数
    """
    url = "https://notify-api.line.me/api/notify"   # LINE notify url
    token = "u8sR52QyZ9k34UCoxIpzBeTP1QT4DfTtO7S2doPJYQI"   # アクセストークン
    
    # 画像もLINEで送る job.pyと同じディレクトリにpictureディレクトリを置いている
    # folderpath = "./picture/"
    # pic_list = os.listdir(folderpath)
    # n = np.random.randint(0, len(pic_list))
    
    headers = {"Authorization" : "Bearer " + token}
    message = "各カード会社のスクレイピングを終了しました"
    payload = {"message": message}
    # files = {"imageFile": open(folderpath + pic_list[n], "rb")}
    
    res = requests.post(url, headers=headers, params=payload)
    
    
if __name__ == "__main__":
    pass