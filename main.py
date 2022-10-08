from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import requests

app = FastAPI()

class Item(BaseModel):
  memberNo: str
  pcId: str
  worldNo: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/html/char/{char_id}")
def get_html(char_id: str):
    url = 'https://lostark.game.onstove.com/Profile/Character/' + char_id   
    r = requests.get(url)
    return r.text

@app.post("/html/collection")
def get_col_html(body: Item):
    data = jsonable_encoder(body)
    url = 'https://lostark.game.onstove.com/Profile/GetCollection'   
    r = requests.post(url, data=data)
    return r.text