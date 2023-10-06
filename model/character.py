from typing import List, Optional
from pydantic import BaseModel

"""
Base Unit
"""
class BaseKeyVal(BaseModel):
    name: str = ""
    value: int = 0

class ItemInfo(BaseModel):
    src: str = ""       # 이미지 경로
    color: str = ""     # 이미지 색상


"""
Advanced Unit
"""
# 기본 정보
class BasicInfo(BaseModel):
    server: str = ""
    job: str = ""
    nickname: str = ""    
    itemLv: str = ""

    isSafe: bool = True
    link: str = ""

    atk: int = 0
    hp: int = 0
    
    fightLv: int = 0    # 전투렙
    skillPt: int = 0
    maxSkillPt: int = 0
    
    adventureLv: int = 0  # 원대렙

# 장비 개별 정보
class Clothes(ItemInfo):
    name: str = ""
    quality: int = 0
    level: int = 0
    set: str = ""
    setLv: int = 1

# 장비 통합 정보
class EquipInfo(BaseModel):
    defense: List[Clothes] = []
    weapon: Optional[Clothes] = None
    defenseCut: int = 0         # 방컷
    defAvgQuality: float = 0    # 방어구 평균 품질
    setName: str = ""           # 세트 조합 (ex. 2악4지)
    setLv: str = ""             # 세트 레벨

# 악세 정보
class Accessory(ItemInfo):
    name: str = ""
    quality: int = 0   # 품질

# 팔찌 정보
class Brace(ItemInfo):
    name: str = ""
    options: List[str] = []

# 악세, 팔찌 통합 정보
class SubEquipInfo(BaseModel):
    accessory: List[Accessory] = []
    brace: Optional[Brace] = None
    accAvgQuality: float = 0    # 악세 평균 품질
    stats: List[BaseKeyVal] = []          # 전투 특성
    imprintings: List[BaseKeyVal] = []       # 각인
    imprintSummay: str = ""

# 보석 정보    
class Jewel(ItemInfo):
    name: str = ""       # 보석 이름
    desc: str = ""      # 보석 효과
    level: int = 1

# 개별 트포 정보
class Tripod(BaseModel):
    originSkill: str = ""
    name: str = ""
    level: int = 1
    isMax: bool = False
    src: str = ""

# 트라이포드 정보
class TripodInfo(BaseModel):
    lv5Tripod: int = 0
    lv4Tripod: int = 0
    maxTripod: int = 0
    tripodList: List[Tripod] = []

class CharInfo(BaseModel):
    basicInfo : Optional[BasicInfo] = None
    collectInfo : List[BaseKeyVal] = []
    equipInfo: Optional[EquipInfo] = None
    subEquipInfo: Optional[SubEquipInfo] = None
    jewelInfo: List[Jewel] = []
    tripodInfo: Optional[TripodInfo] = None
    cardInfo: List[str] = []                   # 카드 효과