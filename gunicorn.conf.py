import os
import sys
from api.function import price_save
from threading import Timer

timer = Timer()

def on_starting(server):
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
    except OSError:
        print ('Failed to make directory')
    timer = Timer(60, price_save, [timer])
    timer.start()

def on_exit(server):
    timer.cancel()
    sys.exit()