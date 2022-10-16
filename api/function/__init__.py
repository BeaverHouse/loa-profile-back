from typing import List
from bs4 import BeautifulSoup
import re
import requests

from model import BaseKeyVal, ClothesInfo, JewelInfo, MainEquipInfo, MainInfo


INT_REGEX = "\D"
TAG_REGEX = "<[^>]*>"

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
    info: List[BaseKeyVal] = []

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

def parseStat(bs: BeautifulSoup) -> List[BaseKeyVal]:
    info: List[BaseKeyVal] = []

    collections = bs.select_one(".profile-ability-battle").select("span")
    for i in range(len(collections)//2):
        e = BaseKeyVal()
        e.name = collections[2*i].text
        e.value = int(collections[2*i+1].text)
        info.append(e)

    info.sort(key=lambda x: x.value, reverse=True)        
    return info

def parseImprint(bs: BeautifulSoup) -> List[BaseKeyVal]:
    info: List[BaseKeyVal] = []

    collections = bs.select_one(".profile-ability-engrave").select("span")
    for c in collections:
        e = BaseKeyVal()
        e.name = c.text.split("Lv.")[0].strip()
        e.value = int(re.sub(INT_REGEX, "", c.text))
        info.append(e)
  
    return info

def parseJewel(j) -> List[JewelInfo]:
    info: List[JewelInfo] = []

    jewels = list(filter(lambda x: "보석" in x["Element_000"]["value"], j["Equip"].values()))

    jewels.sort(key=lambda x: -1 if "멸화" in x["Element_000"]["value"] else 1)

    for a in jewels:
        e = JewelInfo()
        e.level = int(a["Element_001"]["value"]["slotData"]["rtString"].replace("Lv.", ""))
        e.src = 'https://cdn-lostark.game.onstove.com/' + a["Element_001"]["value"]["slotData"]["iconPath"]
        e.desc = re.sub(TAG_REGEX, '', a["Element_004"]["value"]["Element_001"])
        e.name = re.sub(TAG_REGEX, '', a["Element_000"]["value"])
        e.color = a["Element_000"]["value"].split("'")[3]

        info.append(e)
    
    info.sort(key=lambda x: -1 if "멸화" in x.name else 1)
    info.sort(key=lambda x: x.level, reverse=True)
  
    return info

def parseCard(j) -> List[str]:
    info: List[str] = []

    cards = j["CardSet"].values()
    for c in cards:
        effect = list(c.values())[-1]['title'].replace("각성합계)", "각)")
        info.append(effect)

    return info

def parseEquip(j) -> MainEquipInfo:
    info = MainEquipInfo()
    defInfo : List[ClothesInfo] = []
    eqs = list(filter(lambda x: "아이템 레벨" in x["Element_001"]["value"]["leftStr2"], list(j["Equip"].values())))
    for idx, e in enumerate(eqs):
        c = ClothesInfo()
        c.name = re.sub(TAG_REGEX, "", e["Element_000"]["value"])
        
        setInfo = list(filter(lambda x: "ItemPartBox" == x["type"], list(e.values())))[2]
        if('동일한' in str(setInfo)):
            c.set, c.setLv = "에스더", 0
        else: 
            c.set, c.setLv = re.sub(TAG_REGEX, "", setInfo["value"]["Element_001"]).split(" Lv.")

        c.quality = e["Element_001"]["value"]["qualityValue"]
        c.src = 'https://cdn-lostark.game.onstove.com/' + e["Element_001"]["value"]["slotData"]["iconPath"]
        c.color = e["Element_000"]["value"].split("'")[3]

        if idx == 0:
            info.weapon = c
        else:
            defInfo.append(c)
    
    info.defense = defInfo
    return info