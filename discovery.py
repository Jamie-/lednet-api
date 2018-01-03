from threading import Thread, Event
import socket
import json

PORT = 50000 # Server port
INDICATOR = "LEDnet" # Indicator packet is for LEDnet

_stop_event = Event()

def discover():
    print "[INFO] Starting discovery thread..."
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP socket
    s.bind(('', PORT)) # Bind to port

    d = {} # Data to send back to client upon searching for server
    d['hostname'] = socket.gethostname() # Get this hostname
    d['ip'] = socket.gethostbyname(d['hostname']) # Get this IP
    s.settimeout(1.0)

    # Handle incoming broadcasts
    while not is_stopped():
        try:
            data, addr = s.recvfrom(1024) # Wait for a packet
            if data == INDICATOR:
                print "[INFO] Discovery request from {}:{}".format(addr[0], addr[1])
                s.sendto(json.dumps(d), (addr[0], addr[1]))
        except socket.timeout as e:
            pass

##
# Thread Control
##

t = Thread(target=discover)

def start():
    t.start()

def is_stopped():
    return _stop_event.is_set()

def stop():
    _stop_event.set()
    t.join()
