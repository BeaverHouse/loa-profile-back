import json
from model.character import CharInfo
from fastapi import APIRouter, HTTPException
# from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from api.function.v3char import *

# load_dotenv()

router = APIRouter(
    prefix="/v3", tags=["V3"]
)


@router.get("/guardian/price")
def get_guardian_price():
    with open("data/guardian_price.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    
    return data
    

@router.get("/char/{char_id}", response_model=CharInfo)
def get_info(char_id: str):
    url = 'https://lostark.game.onstove.com/Profile/Character/' + char_id
    
    r = requests.get(url)
    bsObject = BeautifulSoup(r.text, "lxml")
    
    jobElement = bsObject.select_one('.profile-character-info__img')
    if(not jobElement):
        raise HTTPException(status_code=404)

    varScript= list(filter(lambda x: "$.Profile =" in x.text, bsObject.select("script")))
    j = json.loads(varScript[0].text.replace("$.Profile =", "").replace(";", ""))
    
    info = CharInfo()
    
    info.basicInfo = parseBasic(bsObject)

    url = 'https://developer-lostark.game.onstove.com/characters/{}/siblings'.format(char_id)
    r = requests.get(url, headers=get_header(), verify=False)

    info.collectInfo = parseCollect(char_id)
    info.equipInfo = parseEquip(j)
    info.subEquipInfo = parseSubEquip(j, bsObject)

    info.jewelInfo = parseJewel(j)
    info.tripodInfo = parseTripod(j)
    info.cardInfo = parseCard(j)

    return info