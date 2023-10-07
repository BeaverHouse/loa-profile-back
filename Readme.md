# LOA Profile B/E
**231007 Code Fixed**   

&#10060; No more major Updates...   
특별한 계기가 없다면, 큰 변경사항 없이 서버만 유지할 계획입니다.

Hosting : [Google Cloud Platform][ref1], e2-micro (10/07 ~ )

**http://api.loaprofile.com**

<br>

## Command
```
# for development
uvicorn main:app

# You need gunicorn to deploy on production 
gunicorn main:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker --daemon
```


[ref1]: https://cloud.google.com/?hl=en
