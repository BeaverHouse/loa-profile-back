from pydantic import BaseModel
from typing import List

class ItemPriceInfo(BaseModel):
    name: str
    code: int
    price: float = 0

class GuardianResponse(BaseModel):
    data: List[ItemPriceInfo]
    time: str