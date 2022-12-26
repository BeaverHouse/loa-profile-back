from .item import get_price_list, price_save

# def parseSafe(bs: BeautifulSoup, arcBs: BeautifulSoup):
#     isSafe = True
#     reason = "정상적인 유저입니다."

#     targetChars = []
#     charAllContent = bs.select(".profile-character-list__char")
#     for all in charAllContent:
#         for c in all.select("li"):
#             targetChars.append(c.select_one("span").select_one("span").text)

#     # 사건사고 조회
#     probCharContent = arcBs.select_one(".article-content").text.split("-")
#     for idx, i in enumerate(probCharContent):
#         if("캐릭터명" in i):
#             probChars = list(map(lambda x: re.sub(SPE_REGEX, "", x), i.split(":")[1].strip().split(" ")))
#             probChars = list(filter(lambda x: len(x)>1, probChars))
#             for t in targetChars:
#                 if t in probChars:
#                     isSafe = False
#                     reason = re.sub(r'http\S+', '', probCharContent[idx+1]).replace("`", "").strip()
#                     return isSafe, reason

#     return isSafe, reason