#!/bin/bash

# Caution : It may not work properly...

sudo apt update
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install gunicorn -y
pip install -r requirements.txt
# sudo gunicorn main:app --bind 0.0.0.0:80 --workers 4 --worker-class uvicorn.workers.UvicornWorker --daemon
gunicorn main:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker --daemon