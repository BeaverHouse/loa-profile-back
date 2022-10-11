# LOA Profile 백엔드
로아 공홈 CORS 문제로 인한 우회 서버용 코드


## Command
```
# for development
uvicorn main:app --reload

# or production
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --daemon
```