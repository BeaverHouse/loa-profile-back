import os
import requests
# from dotenv import load_dotenv
import datetime
from typing import List
from threading import Timer
import json

# load_dotenv()

req_headers = {
    "authorization": "bearer " + os.getenv("LOA_API_KEY", "")
}

def get_price_list(codes: List[int]):
    arr = [] 

    for code in codes:
        url = 'https://developer-lostark.game.onstove.com/markets/items/{}'.format(code)
        data = requests.get(url, headers=req_headers)
        json = data.json()
    
        e = {}
        e["code"] = code
        e["name"] = json[0]["Name"]
        e["price"] = json[0]["Stats"][0]["AvgPrice"]
        if code // 1000 == 66102: # 파괴석, 수호석 필터
            e["price"] = e["price"] / 10
        arr.append(e)

    return {
        "data": arr,
        'time': datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
    }

def price_save(t: Timer):
    arr = [
        66110222, 66110223, 66110224,
        66102003, 66102004, 66102005, 66102105,
        101171, 101912, 101916, 101042, 101221, 101151
    ]

    data = None
    try:
        data = get_price_list(arr)
        with open("data/guardian_price.json", "w", encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
    
    t = Timer(1200, price_save, [None])
    t.daemon = True
    t.start()
