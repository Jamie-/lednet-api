from threading import Thread, Event
from data import LEDnet
import time

_stop_event = Event()

def watch():
    print "[ OK ] Started clock watcher."
    current_time = 0
    while not (is_stopped()):
        time.sleep(1)
        current_time += 1
        if (current_time >= 60):
            current_time = 0
            # Code to run each minute

##
# Thread Control
##

t = Thread(target=watch)

def start():
    print "[INFO] Starting clock watcher..."
    t.start()

def is_stopped():
    return _stop_event.is_set()

def stop():
    _stop_event.set()
    t.join()

# needs:
# - list of strips (so that output and setting to night can be done)
# - day/night cycle times from config
# - night time colour setting (way to change this from API would be useful, persistent changes useful too!)
