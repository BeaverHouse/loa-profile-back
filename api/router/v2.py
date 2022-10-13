from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup
from api.function import parseCollect, parseMain
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

    return info