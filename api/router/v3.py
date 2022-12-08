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

@router.get("/guardian/price")
def get_guardian_price():
    with open("data/guardian_price.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    
    return data
