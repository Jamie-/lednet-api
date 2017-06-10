#!/usr/bin/python
import os
import json
import http
import signal
import sys
from strip import Strip

# Get directory
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Read config file
with open(os.path.join(__location__, 'config.json')) as config_file:
    config = json.load(config_file)
    
# Init list of strips in this system
strips = []
        
# Save state
def save_state():
    print "[INFO] Saving data..."
    save_data = {}
    save_data['strips'] = []
    for s in strips:
        save_data['strips'].append({"red": s.getR(), "green": s.getG(), "blue": s.getB()})
    with open(save_file_path, 'w') as save_file:
        json.dump(save_data, save_file)
    print "[ OK ] Data saved."
    
# Add SIGINT handler (for ctrl-c interrupt)
def sigint_handler(signum, frame):
    save_state()
    print "[INFO] LEDnet now quitting."
    sys.exit()
    
signal.signal(signal.SIGINT, sigint_handler)

# Main
if (__name__) == '__main__':
    # Print splash
    print " _     _____ ____             _"
    print "| |   | ____|  _ \\ _ __   ___| |_"
    print "| |   |  _| | | | | '  \\ / _ \\ __|"
    print "| |___| |___| |_| | | | |  __/ |_"
    print "|_____|_____|____/|_| |_|\\___|\\__|"
    print
    print "Welcome to LEDnet!"
    print
    
    # Load save
    save_file_path = os.path.join(__location__, 'led.json')
    if (os.path.isfile(save_file_path)):
        # Load saved strips from disk
        print "[INFO] Save file found. Loading..."
        with open(save_file_path) as save_file:
            save_data = json.load(save_file)
            for s in save_data['strips']:
                strips.append(Strip(r=s['red'], g=s['green'], b=s['blue']))
            print "[ OK ] Data loaded."
    else:
        # Fill with blank strips
        print "[INFO] No save file found. Starting blank."
        for i in range(config["stripQty"]):
            strips.append(Strip())
    
    # Start HTTP server
    http.config = config
    http.strips = strips
    http.start_server()