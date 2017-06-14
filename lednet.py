#!/usr/bin/python
import os
import json
import http
import signal
import sys
from data import LEDnet
from strip import Strip

# Set paths
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
save_file_path = os.path.join(__location__, 'led.json')
config_file_path = os.path.join(__location__, 'config.json')

# Read config file
def load_config():
    try:
        with open(config_file_path) as config_file:
            print "[ OK ] Config loaded sucessfully."
            return json.load(config_file)
    except IOError:
        print "[ERROR] Unable to load config file, quitting."
        sys.exit(1)

# Load save into strip_array
def load_save(strip_array):
    if (os.path.isfile(save_file_path)):
        # Make list of strip IDs in config
        ids = []
        for i in LEDnet.config["strips"]:
            ids.append(i['id'])
        # Load saved strips from disk
        print "[INFO] Save file found. Loading..."
        with open(save_file_path) as save_file:
            save_data = json.load(save_file)
            for s in save_data['strips']:
                if (s['id'] in ids): # Remove entries not in config
                    strip_array.append(Strip(s['id'], r=s['red'], g=s['green'], b=s['blue']))
            print "[ OK ] Data loaded."
    else:
        # Fill with blank strips
        print "[INFO] No save file found. Starting blank."
        for s in LEDnet.config["strips"]:
            strip_array.append(Strip(s["id"]))
        
# Save state
def save_state():
    print "[INFO] Saving data..."
    save_data = {}
    save_data['strips'] = []
    for s in LEDnet.strips:
        save_data['strips'].append({"id": s.getId(), "red": s.getR(), "green": s.getG(), "blue": s.getB()})
    with open(save_file_path, 'w') as save_file:
        json.dump(save_data, save_file)
    print "[ OK ] Data saved."
    
# Add SIGINT handler (for ctrl-c interrupt)
def sigint_handler(signum, frame):
    save_state()
    print "[INFO] LEDnet now quitting..."
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
    
    # Load config
    LEDnet.config = load_config()
    
    # Load save
    load_save(LEDnet.strips)
    
    # Start HTTP server
    http.start_server()
