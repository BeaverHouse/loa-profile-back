import json
from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup
from api.function import parseCard, parseCollect, parseEquip, parseImprint, parseJewel, \
    parseMain, parseSafe, parseSimpleEquip, parseStat, parseSubEquip, parseSkill
from model import CharInfo

router = APIRouter(
    prefix="/v2", tags=["V2"]
)


@router.get("/char/{char_id}", response_model=CharInfo)
def get_info(char_id: str):
    url = 'https://lostark.game.onstove.com/Profile/Character/' + char_id
    
    r = requests.get(url)
    bsObject = BeautifulSoup(r.text, "lxml")
    
    jobElement = bsObject.select_one('.profile-character-info__img')
    if(not jobElement):
        raise HTTPException(status_code=404, detail="해당하는 캐릭터가 없습니다.")
    
    info = CharInfo()

    info.mainInfo = parseMain(bsObject)
    info.collectInfo = parseCollect(bsObject)
    info.statInfo = parseStat(bsObject)
    info.imprintingInfo = parseImprint(bsObject)

    varScript= list(filter(lambda x: "$.Profile =" in x.text, bsObject.select("script")))
    j = json.loads(varScript[0].text.replace("$.Profile =", "").replace(";", ""))
    
    info.jewelInfo = parseJewel(j)
    info.card = parseCard(j)
    info.equipInfo = parseEquip(j)
    info.subEquipInfo = parseSubEquip(j)

    info.simpleEquipInfo = parseSimpleEquip(info.equipInfo, info.subEquipInfo)

    url2 = 'https://arca.live/b/lostark/53703658'
    
    r2 = requests.get(url2)
    arcBsObject = BeautifulSoup(r2.text, "lxml")
    info.isSafe, info.reason = parseSafe(bsObject, arcBsObject)

    info.skillInfo = parseSkill(bsObject, j)

    return info