import json
from model.character import CharInfo
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from api.function.v3char import *
from firebase_admin import firestore
import base64

load_dotenv()

router = APIRouter(
    prefix="/v3", tags=["V3"]
)


@router.get("/guardian/price")
def get_guardian_price():
    with open("data/guardian_price.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    
    return data

@router.post("/char/block")
def block(user: BlockUser):

    try:
        decoded = base64.b64decode(user.key).decode('utf-8')
    except:        
        return HTTPException(status_code=400, detail="키 값 오류입니다.")

    if decoded != os.getenv("SECRET_KEY"):
        return HTTPException(status_code=400, detail="키 값 오류입니다.")
    
    db = firestore.client()
    url = 'https://developer-lostark.game.onstove.com/characters/{}/siblings'.format(user.name)
    r = requests.get(url, headers=get_header(), verify=False)

    chars = r.json()
    count = 0
    arr = []
    for c in chars:
        doc_ref = db.collection("lostark_block").document(c["CharacterName"])
        if not doc_ref.get().exists:
            count += 1
            arr.append(c["CharacterName"])
        doc_ref.set({
            "link": user.link
        })

    return {
        "target": user.name,
        "link": user.link,
        "processCount": count,
        "charList": arr
    }
    

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

    db = firestore.client()
    chars = r.json()
    for c in chars:
        doc_ref = db.collection("lostark_block").document(c["CharacterName"])
        if doc_ref.get().exists:
            info.basicInfo.isSafe = False
            info.basicInfo.link = doc_ref.get().to_dict()["link"]

    info.collectInfo = parseCollect(char_id)
    info.equipInfo = parseEquip(j)
    info.subEquipInfo = parseSubEquip(j, bsObject)

    info.jewelInfo = parseJewel(j)
    info.tripodInfo = parseTripod(j)
    info.cardInfo = parseCard(j)

    return info

@router.get("/char/{char_id}/electron", response_model=CharInfo)
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

    db = firestore.client()
    chars = r.json()
    for c in chars:
        doc_ref = db.collection("lostark_block").document(c["CharacterName"])
        if doc_ref.get().exists:
            info.basicInfo.isSafe = False
            info.basicInfo.link = doc_ref.get().to_dict()["link"]

    info.equipInfo = parseEquip(j)
    info.subEquipInfo = parseSubEquip(j, bsObject)

    info.jewelInfo = parseJewel(j)
    info.tripodInfo = parseTripod(j)
    info.cardInfo = parseCard(j)

    return info