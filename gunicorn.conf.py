import os
import sys
from api.function import price_save
from threading import Timer

def on_starting(server):
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
    except OSError:
        print ('Failed to make directory')
    price_save(None)

def on_exit(server):
    sys.exit()