from typing import List
from bs4 import BeautifulSoup
import re
import requests

from model import BaseKeyVal, MainInfo


INT_REGEX = "\D"
TAG_REGEX = "(<([^>]+)>)"

def parseMain(bs: BeautifulSoup) -> MainInfo:
    main = MainInfo()

    main.server = bs.select_one(".profile-character-info__server").text.replace("@", "")
    main.nickname = bs.select_one(".profile-character-info__name").text.replace("@", "")
    main.job = bs.select_one(".profile-character-info__img").attrs["alt"]

    statData = bs.select_one(".profile-ability-basic").select("span")
    main.atk = statData[1].text
    main.hp = statData[3].text

    main.fightLv = int(re.sub(INT_REGEX, "", bs.select_one(".profile-character-info__lv").text))
    main.itemLv = float(bs.select_one(".level-info2__expedition").text
        .replace("장착 아이템 레벨Lv.", "").replace(",", ""))
    main.partyLv = int(re.sub(INT_REGEX, "", bs.select_one(".level-info__expedition").text))
    
    return main

def parseCollect(bs: BeautifulSoup) -> List[BaseKeyVal]:
    info = []

    varScript= list(filter(lambda x: "var _memberNo" in x.text, bs.select("script")))
    vars = varScript[0].text.split("\r\n\t\t")[:4]
    
    memberNo = vars[1].split("= '")[-1].replace("';", "")
    pcId = vars[2].split("= '")[-1].replace("';", "")
    worldNo = vars[3].split("= '")[-1].replace("';", "")

    url = 'https://lostark.game.onstove.com/Profile/GetCollection'   
    r = requests.post(url, data=({
        'memberNo': memberNo,
        'pcId': pcId,
        'worldNo': worldNo
    }))

    new_bs = BeautifulSoup(r.text, "lxml")

    collections = new_bs.select_one(".lui-tab__menu").select("a")
    for c in collections:
        e = BaseKeyVal()
        e.name = " ".join(c.text.split(" ")[:-1])
        e.value = int(re.sub(INT_REGEX, "", c.text))
        info.append(e)
        
    return info
