from threading import Thread, Event
from datetime import datetime
from data import LEDnet
from cycle import Cycle
from time import sleep
import operator

_stop_event = Event()

def watch():
    print "[INFO] Loading clock watcher..."

    cycles = []
    for c in LEDnet.config["cycles"]:
        time = datetime.strptime(c["start"], "%H:%M.%S").time()
        # Set strip target
        target = None
        if not (c["target"] == "global"):
            for s in LEDnet.config["strips"]:
                if (s["id"] == c["target"]):
                    target = s
                    break
        if (c["mode"] == "static"):
            cycles.append(Cycle(c["name"], c["mode"], target, time, values=c["values"]))
        else:
            cycles.append(Cycle(c["name"], c["mode"], target, time))
    cycles.sort(key=operator.attrgetter('time'), reverse=True) # Sort cycles by time (reversed)

    tick_time = 0 # Tick loop counter
    current_cycle = None
    sleep(2) # Wait for serial ports to open
    print "[ OK ] Started clock watcher."
    while not (is_stopped()):
        if (tick_time == 0): # Run once a tick
            now = datetime.now().time()
            for c in cycles:
                if (now >= c.get_time()): # Check if cycle should have started
                    # Do not change output if cycle already active
                    if (current_cycle == None) or (current_cycle.get_name() != c.get_name()):
                        print "[WTCH] Incrementing cycle to " + str(c.get_name()) + "."
                        set_cycle(c)
                        current_cycle = c
                    break # Exit cycle time-check loop as time has been found
            if (current_cycle == None): # If started up before first cycle
                print "[WTCH] Incrementing cycle to " + str(cycles[0].get_name()) + "."
                current_cycle = cycles[0]
                set_cycle(cycles[0])
        tick_time += 1 # Increment tick counter
        if (tick_time > 60): # Set tick as 60s
            tick_time = 0
        sleep(1)

def set_cycle(c):
    if (c.get_target() == None): # Global cycle
        for s in LEDnet.strips:
            if (c.get_mode() == "static"):
                v = c.get_values()
                s.set_mode(c.get_mode(), r=v["red"], g=v["green"], b=v["blue"])
            else:
                s.set_mode(c.get_mode())
    else: # Single strip cycle
        if (c.get_mode() == "static"):
            v = c.get_values()
            c.get_target().set_mode(c.get_mode(), r=v["red"], g=v["green"], b=b["blue"])
        else:
            c.get_target().set_mode(c.get_mode())

##
# Thread Control
##

t = Thread(target=watch)

def start():
    t.start()

def is_stopped():
    return _stop_event.is_set()

def stop():
    _stop_event.set()
    t.join()
