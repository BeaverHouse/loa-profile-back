from dotenv import load_dotenv
import os
import datetime
from typing import List
import requests
from model import BaseKeyVal

load_dotenv()

INT_REGEX = "\D"

def get_header():
    token = datetime.datetime.now().microsecond % 3
    if token == 0:
        return {
            "authorization": "bearer " + os.getenv("LOA_API_KEY", "")
        }
    else:
        return {
            "authorization": "bearer " + os.getenv("LOA_API_KEY_2", "")
        }

def v3parseCollect(char_id: str) -> List[BaseKeyVal]:
    info: List[BaseKeyVal] = []

    url = 'https://developer-lostark.game.onstove.com/armories/characters/{}/collectibles'.format(char_id) 
    r = requests.get(url, headers=get_header())

    collections = r.json()
    for c in collections:
        e = BaseKeyVal()
        e.name = c["Type"]
        e.value = c["Point"]
        info.append(e)
        
    return info
