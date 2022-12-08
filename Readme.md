# LOA Profile 백엔드
221208 : OpenAPI 추가작업 진행중   
프로필 부분은 제한해제 승인 시 반영 예정.


로아 공홈 CORS 문제로 인한 우회 서버용 코드

http://api.loaprofile.com/docs

## Command
```
# for development
uvicorn main:app --reload

# or production
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --daemon
```