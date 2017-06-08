#!/usr/bin/python
import os
import json
import http
from strip import Strip

# Read config file
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, 'config.json')) as config_file:
    config = json.load(config_file)

# Init list of strips in this system
strips = []
for i in range(config["stripQty"]):
    strips.append(Strip())

# Main
if (__name__) == '__main__':
    # Start HTTP server
    http.config = config
    http.strips = strips
    http.start_server()