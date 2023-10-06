# LOA Profile B/E
231006 Code Clean   
No more Updates

http://api.loaprofile.com

## Command
```
# for development
uvicorn main:app

# or production
sudo gunicorn main:app --bind 0.0.0.0:80 --workers 4 --worker-class uvicorn.workers.UvicornWorker --daemon
```