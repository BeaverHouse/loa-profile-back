from typing import List
from bs4 import BeautifulSoup
import re
import requests
from api.function.constant import EFFECT_BRACE

from model import AccessoryInfo, BaseKeyVal, BraceInfo, ClothesInfo, \
    JewelInfo, MainEquipInfo, MainInfo, SimpleEquipInfo, SubEquipInfo, SkillInfo, TripodInfo


INT_REGEX = "\D"
TAG_REGEX = "<[^>]*>"
SPE_REGEX = r"[^\uAC00-\uD7A30-9a-zA-Z\s]"

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

    jewels = list(filter(lambda x: "보석" in x["Element_001"]["value"]["leftStr0"], j["Equip"].values()))

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
            info.weapon = c
        else:
            defInfo.append(c)
    
    info.defense = defInfo
    return info

def parseSubEquip(j) -> SubEquipInfo:
    info = SubEquipInfo()

    accInfo : List[AccessoryInfo] = []
    accs = list(filter(lambda x: "무작위 각인" in str(x.get("Element_006")) \
    and "세공" not in str(x.get("Element_005")), list(j["Equip"].values())))
    
    for acc in accs:
        i = AccessoryInfo()
        i.name = re.sub(TAG_REGEX, "", acc["Element_000"]["value"])
        i.quality = acc["Element_001"]["value"]["qualityValue"]
        i.src = 'https://cdn-lostark.game.onstove.com/' + acc["Element_001"]["value"]["slotData"]["iconPath"]
        i.color = acc["Element_000"]["value"].split("'")[3]
        accInfo.append(i)

    info.accessory = accInfo

    brace = BraceInfo()
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

    info.brace = brace

    return info

def parseSimpleEquip(main: MainEquipInfo, sub: SubEquipInfo) -> SimpleEquipInfo:
    info = SimpleEquipInfo()
    info.weapon = main.weapon
    info.brace = sub.brace
    info.defenseCut = min(list(map(lambda x: x.level, main.defense)))
    info.defenseSrc = main.defense[1].src
    info.accSrc = sub.accessory[0].src if len(sub.accessory) == 5 else "" 
    
    dic = {}
    levelArr = []
    topLevel = 0
    for d in main.defense:
        dic[d.set] = dic.get(d.set, 0) + 1
        levelArr.append(99 if d.set == "에스더" else d.setLv)
        if d.setLv > topLevel:
            topLevel = d.setLv

    d = main.weapon
    dic[d.set] = dic.get(d.set, 0) + 1
    levelArr.append(99 if d.set == "에스더" else d.setLv)
    if d.setLv > topLevel:
        topLevel = d.setLv
    
    levelArr.sort(reverse=True)
    info.setName = ""
    for i in dic.keys():
        info.setName += " {}{}".format(dic[i], i)
    info.setName = info.setName.strip()
    info.setLv = '{}레벨 {}세트'.format(topLevel, levelArr.count(topLevel) + levelArr.count(99)) if topLevel > 0 else "세트 효과 없음"

    accQList = list(map(lambda x: x.quality, sub.accessory))
    if(len(accQList) == 5):
        info.accAvgQuality = (accQList[0]*10 + accQList[1]*3 + accQList[2]*3 + accQList[3]*2+ accQList[4]*2) / 20.0
    info.defAvgQuality = sum(list(map(lambda x: x.quality, main.defense))) / 5.0

    return info

def parseSafe(bs: BeautifulSoup, arcBs: BeautifulSoup):
    isSafe = True
    reason = "정상적인 유저입니다."

    targetChars = []
    charAllContent = bs.select(".profile-character-list__char")
    for all in charAllContent:
        for c in all.select("li"):
            targetChars.append(c.select_one("span").select_one("span").text)

    # 사건사고 조회
    probCharContent = arcBs.select_one(".article-content").text.split("-")
    for idx, i in enumerate(probCharContent):
        if("캐릭터명" in i):
            probChars = list(map(lambda x: re.sub(SPE_REGEX, "", x), i.split(":")[1].strip().split(" ")))
            probChars = list(filter(lambda x: len(x)>1, probChars))
            for t in targetChars:
                if t in probChars:
                    isSafe = False
                    reason = re.sub(r'http\S+', '', probCharContent[idx+1]).replace("`", "").strip()
                    return isSafe, reason

    return isSafe, reason

def parseSkill(bs: BeautifulSoup, j) -> SkillInfo:
    info = SkillInfo()
    collections = bs.select_one(".profile-skill__point").select("em")
    info.skillPt = collections[0].text
    info.maxSkillPt = collections[1].text

    skillData = list(j["Skill"].values())
    t4,t5,mt = 0,0,0
    tripodArr = []
    for s in skillData:
        skillLv = int(re.sub(INT_REGEX, "", s["Element_003"]["value"]))
        if skillLv >= 4:
            skillNm = s["Element_000"]["value"]
            for tripod in list(s["Element_006"]["value"].values()):
                tName = re.sub(TAG_REGEX, "", tripod["name"])
                if len(tName) > 0:                
                    t = TripodInfo()
                    t.originSkill = skillNm
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

    info.tripodList = tripodArr
    info.lv4Tripod = t4
    info.lv5Tripod = t5
    info.maxTripod = min(18, mt)

    return info