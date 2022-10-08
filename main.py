from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

origins = [
    "https://beaverhouse.github.io",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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