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
    cycles.sort(key=operator.attrgetter('time')) # Sort cycles by time

    tick_time = 0 # Tick loop counter
    current_cycle = None
    sleep(2) # Wait for serial ports to open
    print "[ OK ] Started clock watcher."
    while not (is_stopped()):
        if (tick_time == 0): # Run once a tick
            now = datetime.now().time()
            prev = None # Previous cycle in loop
            for c in cycles:
                if not(prev == None): # Loop works off of last seen cycle and uses 'c' to test with
                    if (c.get_time() > now >= prev.get_time()):
                        # Do not change output if cycle already active
                        if (current_cycle == None) or (current_cycle.get_name() != prev.get_name()):
                            print "[WTCH] Incrementing cycle to " + str(prev.get_name()) + "."
                            if (prev.get_target() == None): # Global cycle
                                for s in LEDnet.strips:
                                    if (prev.get_mode() == "static"):
                                        v = prev.get_values()
                                        s.set_mode(prev.get_mode(), r=v["red"], g=v["green"], b=v["blue"])
                                    else:
                                        s.set_mode(prev.get_mode())
                            else: # Single strip cycle
                                if (prev.get_mode() == "static"):
                                    v = prev.get_values()
                                    prev.get_target().set_mode(prev.get_mode(), r=v["red"], g=v["green"], b=b["blue"])
                                else:
                                    prev.get_target().set_mode(prev.get_mode())
                            current_cycle = prev
                        break # Exit cycle time-check loop as time has been found
                prev = c
        tick_time += 1 # Increment tick counter
        if (tick_time > 60): # Set tick as 60s
            tick_time = 0
        sleep(1)
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
