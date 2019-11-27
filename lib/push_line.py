import json
import requests
import numpy as np
import os


def push_line(message):
    """
    LINE通知用関数
    filename: str型 LINEへの通知の際のメッセージ内容に書き込んだファイル名を入れている
    """
    with open("../json/line.json", "r") as fr:
        info = json.load(fr)
    
    url = info["url"]  # LINE notify url
    token = info["token"]  # アクセストークン
    
    headers = {"Authorization" : "Bearer " + token}
    payload = {"message": message}
    r = requests.post(url, headers=headers, params=payload)
    
    
if __name__ == "__main__":
    pass
    push_line("Please Money \n お金足りないよ")