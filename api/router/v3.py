import json
from fastapi import APIRouter, HTTPException
import requests
import os
from model import CharInfo
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/v3", tags=["V3"]
)

req_headers = {
    "authorization": "bearer " + os.getenv("LOA_API_KEY", "")
}

@router.get("/test/{char_id}")
def get_info(char_id: str):
    url = 'https://developer-lostark.game.onstove.com/armories/characters/{}/profiles'.format(char_id)
    data = requests.get(url, headers=req_headers)
    
    return data.json()
