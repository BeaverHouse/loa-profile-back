from optparse import Option
from typing import List, Optional
from pydantic import BaseModel

class BaseKeyVal(BaseModel):
    name: str = ""
    value: int = 0

class ItemInfo(BaseModel):
    src: str = ""       # 이미지 경로
    color: str = ""     # 이미지 색상

# 개별 트포 정보
class TripodInfo(BaseModel):
    originSkill: str = ""
    name: str = ""
    level: int = 1
    isMax: bool = False

# 악세 정보
class AccessoryInfo(ItemInfo):
    name: str = ""
    quality: int = 0   # 품질

# 팔찌 정보
class BraceInfo(ItemInfo):
    name: str = ""
    options: List[str] = []

# 보석 정보    
class JewelInfo(ItemInfo):
    name: str = ""       # 보석 이름
    desc: str = ""      # 보석 효과
    level: int = 1

# 방어구, 무기 정보
class ClothesInfo(ItemInfo):
    name: str = ""
    quality: int = 0
    level: int = 0
    set: str = ""
    setLv: int = 1


# 메인 장비 (무기, 방어구)
class MainEquipInfo(BaseModel):
    defense: List[ClothesInfo] = []
    weapon: Optional[ClothesInfo]

# 서브 장비 (악세, 팔찌)
class SubEquipInfo(BaseModel):
    accessory: List[AccessoryInfo] = []
    brace: Optional[BraceInfo]

class SimpleEquipInfo(BaseModel):
    defenseCut: int = 0         # 방컷
    defenseSrc: str = ""        # 방어구 이미지 (상의)
    defAvgQuality: float = 0    # 방어구 평균 품질
    weapon: Optional[ClothesInfo]
    setName: str = ""           # 세트 조합 (ex. 2악4지)
    setLv: str = ""             # 세트 레벨
    accAvgQuality: float = 0    # 악세 평균 품질
    accSrc: str = ""            # 악세 이미지 (목걸이)
    brace: Optional[BraceInfo]

class MainInfo(BaseModel):
    server: str = ""
    job: str = ""
    nickname: str = ""       # 실제 닉네임
    displayName: Optional[str] = None    # 따로 표시할 이름
    atk: int = 0
    hp: int = 0
    fightLv: int = 0    # 전투렙
    itemLv: float = 0
    partyLv: int = 0    # 원대렙

class SkillInfo(BaseModel):
    skillPt: int = 0
    maxSkillPt: int = 0
    lv5Tripod: int = 0
    lv4Tripod: int = 0
    maxTripod: int = 0
    tripodList: List[TripodInfo] = []

class CharInfo(BaseModel):
    mainInfo : Optional[MainInfo]
    collectInfo : List[BaseKeyVal] = []     # 수집형 포인트
    statInfo: List[BaseKeyVal] = []          # 전투 특성
    imprintingInfo: List[BaseKeyVal] = []       # 각인
    jewelInfo: List[JewelInfo] = []
    card: List[str] = []                   # 카드 효과

    equipInfo: Optional[MainEquipInfo]
    subEquipInfo: Optional[SubEquipInfo]
    simpleEquipInfo: Optional[SimpleEquipInfo]
    skillInfo: Optional[SkillInfo]

    isSafe: Optional[bool]      # 사건사고 여부
    reason: Optional[str]       # 사유