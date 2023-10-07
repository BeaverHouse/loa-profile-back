# from dotenv import load_dotenv
import os
import datetime
from typing import List
import re
import requests
from model.character import *
from bs4 import BeautifulSoup
from api.function.constant import EFFECT_BRACE, EFFECT_SET, JOB_BOOKS

# load_dotenv()
    
def get_header():
    token = datetime.datetime.now().microsecond % 5
    if token <= 1:
        return {
            "authorization": "bearer " + os.getenv("LOA_API_KEY", "")
        }
    else:
        return {
            "authorization": "bearer " + os.getenv(f"LOA_API_KEY_{token}", "")
        }

INT_REGEX = "\D"
TAG_REGEX = "<[^>]*>"
SPE_REGEX = r"[^\uAC00-\uD7A30-9a-zA-Z\s]"

def parseBasic(bs: BeautifulSoup) -> BasicInfo:
    res = BasicInfo()

    res.server = bs.select_one(".profile-character-info__server").text.replace("@", "")
    res.job = bs.select_one(".profile-character-info__img").attrs["alt"]
    res.nickname = bs.select_one(".profile-character-info__name").text.replace("@", "")
    res.itemLv = float(bs.select_one(".level-info2__expedition").text
        .replace("장착 아이템 레벨Lv.", "").replace(",", ""))

    statData = bs.select_one(".profile-ability-basic").select("span")
    res.atk = statData[1].text
    res.hp = statData[3].text

    res.fightLv = int(re.sub(INT_REGEX, "", bs.select_one(".profile-character-info__lv").text))
    collections = bs.select_one(".profile-skill__point").select("em")
    res.skillPt = collections[0].text
    res.maxSkillPt = collections[1].text
    res.adventureLv = int(re.sub(INT_REGEX, "", bs.select_one(".level-info__expedition").text))

    return res


def parseEquip(j) -> EquipInfo:
    res = EquipInfo()
    defInfo : List[Clothes] = []
    eqs = list(filter(lambda x: "아이템 레벨" in x["Element_001"]["value"]["leftStr2"], list(j["Equip"].values())))
    for idx, e in enumerate(eqs):
        c = Clothes()
        c.name = re.sub(TAG_REGEX, "", e["Element_000"]["value"])
        c.level = int(re.sub(TAG_REGEX, "", e["Element_001"]["value"]["leftStr2"]).split(" ")[2])
        
        itemPartList = list(filter(lambda x: "ItemPartBox" == x["type"], list(e.values())))
        if len(itemPartList) <= 2:
            c.set, c.setLv = "일반장비", 0
        else:
            setInfo = itemPartList[2]
            if('동일한' in str(setInfo)):
                c.set, c.setLv = "에스더", 0
            else: 
                set, setLv = re.sub(TAG_REGEX, "", setInfo["value"]["Element_001"]).split(" Lv.")
                c.set = set
                c.setLv = int(setLv)

        c.quality = e["Element_001"]["value"]["qualityValue"]
        c.src = 'https://cdn-lostark.game.onstove.com/' + e["Element_001"]["value"]["slotData"]["iconPath"]
        c.color = e["Element_000"]["value"].split("'")[3]

        if idx == 0:
            res.weapon = c
        else:
            defInfo.append(c)
    
    res.defense = defInfo

    res.defenseCut = min(list(map(lambda x: x.level, defInfo))) if len(defInfo) == 5 else 0
    res.defAvgQuality = sum(list(map(lambda x: x.quality, defInfo))) / 5.0

    dic = {}
    levelArr = []
    topLevel = 0
    for d in res.defense:
        dic[d.set] = dic.get(d.set, 0) + 1
        levelArr.append(99 if d.set == "에스더" else d.setLv)
        if d.setLv > topLevel:
            topLevel = d.setLv

    d = res.weapon
    dic[d.set] = dic.get(d.set, 0) + 1
    levelArr.append(99 if d.set == "에스더" else d.setLv)
    if d.setLv > topLevel:
        topLevel = d.setLv
    
    levelArr.sort(reverse=True)
    res.setName = ""
    for i in dic.keys():
        if i in EFFECT_SET:
            res.setName += " {}{}".format(dic[i], i)
    res.setName = res.setName.strip()
    res.setLv = '{}레벨 {}세트'.format(topLevel, levelArr.count(topLevel) + levelArr.count(99)) if topLevel > 0 else "세트 효과 없음"

    return res
    

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

def parseImprint(bs: BeautifulSoup) -> List[ImprintInfo]:
    info: List[ImprintInfo] = []

    collections = bs.select_one(".profile-ability-engrave").select("span")
    for c in collections:
        e = ImprintInfo()
        e.name = c.text.split("Lv.")[0].strip()
        e.value = int(c.text.split("Lv.")[1].strip())
        e.isJob = e.name in JOB_BOOKS
        info.append(e)
  
    return info


def parseSubEquip(j, bs: BeautifulSoup) -> SubEquipInfo:
    res = SubEquipInfo()

    accInfo : List[Accessory] = []
    accs = list(filter(lambda x: "무작위 각인" in str(x.get("Element_006")) \
    and "세공" not in str(x.get("Element_005")), list(j["Equip"].values())))
    
    for acc in accs:
        i = Accessory()
        i.name = re.sub(TAG_REGEX, "", acc["Element_000"]["value"])
        i.quality = acc["Element_001"]["value"]["qualityValue"]
        i.src = 'https://cdn-lostark.game.onstove.com/' + acc["Element_001"]["value"]["slotData"]["iconPath"]
        i.color = acc["Element_000"]["value"].split("'")[3]
        accInfo.append(i)

    res.accessory = accInfo

    brace = Brace()
    braceData = list(filter(lambda x: "팔찌" in x["Element_000"]["value"], list(j["Equip"].values())))
    if len(braceData) > 0:
        b = braceData[0]
        brace.name = re.sub(TAG_REGEX, "", b["Element_000"]["value"])
        brace.src = 'https://cdn-lostark.game.onstove.com/' + b["Element_001"]["value"]["slotData"]["iconPath"]
        brace.color = b["Element_000"]["value"].split("'")[3]

        optInfo = []
        optionArr = b["Element_004"]["value"]["Element_001"].split("<BR>")
        for opt in optionArr:
            parsedOpt = re.sub(TAG_REGEX, "", opt)
            for eff in EFFECT_BRACE:
                if "[{}]".format(eff) in parsedOpt:
                    optInfo.append(eff)
                    break
        brace.options = optInfo

    res.brace = brace

    accQList = list(map(lambda x: x.quality, res.accessory))
    if(len(accQList) == 5):
        res.accAvgQuality = (accQList[0]*10 + accQList[1]*3 + accQList[2]*3 + accQList[3]*2+ accQList[4]*2) / 20.0

    res.stats = parseStat(bs)
    res.imprintings = parseImprint(bs)
    res.imprintSummay = "".join(map(lambda y: str(y.value), filter(lambda x: "감소" not in x.name, res.imprintings)))

    return res


def parseCollect(char_id: str) -> List[BaseKeyVal]:
    res: List[BaseKeyVal] = []

    url = 'https://developer-lostark.game.onstove.com/armories/characters/{}/collectibles'.format(char_id) 
    r = requests.get(url, headers=get_header(), verify=False)

    collections = r.json()
    for c in collections:
        e = BaseKeyVal()
        e.name = c["Type"]
        e.value = c["Point"]
        res.append(e)
        
    return res


def parseJewel(j) -> List[Jewel]:
    res: List[Jewel] = []

    jewels = list(filter(lambda x: "보석" in x["Element_001"]["value"]["leftStr0"], j["Equip"].values()))

    jewels.sort(key=lambda x: -1 if "멸화" in x["Element_000"]["value"] else 1)

    for a in jewels:
        e = Jewel()
        e.level = int(a["Element_001"]["value"]["slotData"]["rtString"].replace("Lv.", ""))
        e.src = 'https://cdn-lostark.game.onstove.com/' + a["Element_001"]["value"]["slotData"]["iconPath"]
        e.name = re.sub(TAG_REGEX, '', a["Element_000"]["value"])
        if "귀속" in e.name:
            e.desc = re.sub(TAG_REGEX, '', a["Element_005"]["value"]["Element_001"])
        else:
            e.desc = re.sub(TAG_REGEX, '', a["Element_004"]["value"]["Element_001"])
        e.color = a["Element_000"]["value"].split("'")[3]

        res.append(e)
    
    res.sort(key=lambda x: -1 if "멸화" in x.name else 1)
    res.sort(key=lambda x: x.level, reverse=True)
  
    return res


def parseTripod(j) -> TripodInfo:
    res = TripodInfo()

    skillData = list(j["Skill"].values())
    t4,t5,mt = 0,0,0
    tripodArr = []
    for s in skillData:
        skillLv = int(re.sub(INT_REGEX, "", s["Element_003"]["value"]))
        if skillLv >= 4:
            tripodTarget = list(filter(lambda x: x["type"] == "TripodSkillCustom", s.values()))
            skillNm = s["Element_000"]["value"]
            skillIcon = 'https://cdn-lostark.game.onstove.com/' + s["Element_001"]["value"]["slotData"]["iconPath"]
            for tripod in list(tripodTarget[0]["value"].values()):
                tName = re.sub(TAG_REGEX, "", tripod["name"])
                if len(tName) > 0:                
                    t = Tripod()
                    t.originSkill = skillNm
                    t.src = skillIcon
                    t.name = tName
                    rawLvData = re.sub(TAG_REGEX, "", tripod["tier"])
                    t.level = int(re.sub(INT_REGEX, "", rawLvData))
                    t.isMax = "최대" in rawLvData
                    if t.level == 5:
                        t5 += 1
                    elif t.level == 4:
                        t4 += 1
                    if not (t.level==1 and t.isMax):
                        mt += 1    
                    tripodArr.append(t)

    res.tripodList = tripodArr
    res.lv4Tripod = t4
    res.lv5Tripod = t5
    res.maxTripod = min(18, mt)

    return res


def parseCard(j) -> List[str]:
    res: List[str] = []

    cards = j["CardSet"].values() if j["CardSet"] else []
    for c in cards:
        if len(c.values()) <= 1:
            continue
        effect = list(c.values())[-1]['title'].replace("각성합계)", "각)")
        res.append(effect)

    return res