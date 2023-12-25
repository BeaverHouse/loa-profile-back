# ⛵ LOA Profile (B/E)

(I'll write README in Korean, because this service is for Korean only)

### ✅ This repository is deployed for production

https://api.loaprofile.com  
Hosting : [Google Cloud Platform][gcp], e2-micro

### ⛔ This repository's code is deprecated

<br>

**Main Stack**  
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)][fastapi]  
It's licensed under the MIT License. see: https://github.com/tiangolo/fastapi

<br>
<br>

## 설명

LOA Profile의 간이 서버 코드입니다.  
2가지의 간단한 API로 구성되어 있습니다.

- 가디언 토벌 수익 계산을 위한 아이템 가격 조회 API  
  가격은 주기적으로 텍스트 파일에 업데이트되고 API는 파일의 내용을 반환합니다.
- 군장검사를 위한 캐릭터 조회 API

현재 [로스트아크][lostark] 게임을 플레이하고 있지 않기 때문에, 더 이상 관리를 하고 있지 않습니다.  
특별한 계기가 없다면, 큰 변경사항 없이 버그 수정/최소한의 유지보수만 할 계획입니다.

<br/>

**Web** : [BeaverHouse/loa-profile-front][web]  
**Windows App** : [BeaverHouse/loa-profile-electron][windows]

<!--If you have latest repository, link here-->

<br>

## Command

따로 작성해 놓은 [Gist][gist]를 참고해 주세요.

[lostark]: https://lostark.game.onstove.com/Main
[fastapi]: https://fastapi.tiangolo.com/
[gcp]: https://cloud.google.com/?hl=en
[web]: https://github.com/BeaverHouse/loa-profile-front
[windows]: https://github.com/BeaverHouse/loa-profile-electron
[gist]: https://gist.github.com/HU-Lee/771ce2427b46801ce186343f55c4bed8

<!--
You can find some emojis at https://html-css-js.com/html/character-codes/
You can find some badges at https://dev.to/envoy_/150-badges-for-github-pnk
-->
