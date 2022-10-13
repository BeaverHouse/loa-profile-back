from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from api.router import v2

tags_metadata = [
    {
        "name": "V1",
        "description": "Returns pure HTML String from Lost Ark Page",
    },
    {
        "name": "V2",
        "description": "Parse specific data from Lost Ark Page",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(v2.router)

origins = [
    "https://beaverhouse.github.io",
    "https://loaprofile.com",
    "https://beta.loaprofile.com",
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


@app.get("/v1/char/{char_id}", tags=["V1"])
def get_html(char_id: str):
    url = 'https://lostark.game.onstove.com/Profile/Character/' + char_id   
    r = requests.get(url)
    return r.text

@app.post("/v1/collection", tags=["V1"])
def get_col_html(body: Item):
    data = jsonable_encoder(body)
    url = 'https://lostark.game.onstove.com/Profile/GetCollection'   
    r = requests.post(url, data=data)
    return r.text