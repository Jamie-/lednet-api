from flask import Flask, abort, request, make_response, jsonify
from strip import Strip
from data import LEDnet
import time
import json

lednet = Flask(__name__)

def get_strip(id):
    for s in LEDnet.strips:
        if (s.getId() == id):
            strip = s
            return s
    return None

##
# Endpoints
##

@lednet.route('/', methods=['GET'])
def get_index():
    return jsonify({"systemName": LEDnet.config["systemName"], "noOfStrips": len(LEDnet.strips)})

@lednet.route('/info', methods=['GET'])
def get_info():
    return jsonify({"system": {"systemName": LEDnet.config["systemName"], "systemTime": time.strftime("%H:%M.%S"), "strips": len(LEDnet.strips), "cycle": "day"}})

@lednet.route('/config', methods=['GET', 'POST'])
def get_config():
    if (request.method == 'GET') and is_auth_needed():
        abort(401)
    if (request.method == 'POST') and is_auth_needed():
        if not (request.json):
            abort(400)
        if not (check_auth(request.json)):
            abort(401)
    return json.dumps(LEDnet.config)

# See system LED data
@lednet.route('/led', methods=['GET'])
def get_led_data():
    return jsonify({"strips": LEDnet.config["strips"]})

# View strip output data
@lednet.route('/led/<string:strip_id>', methods=['GET'])
def get_strip_values(strip_id):
    strip = get_strip(strip_id)
    if (strip == None):
        abort(404)
    return strip.get_data_as_json()

@lednet.route('/led/<string:strip_id>', methods=['POST'])
def set_strip_rgb(strip_id):
    # Check request is JSON
    if not (request.json):
        abort(400)
    # Check for authentication
    if not (check_auth(request.json)):
        abort(401)
    # Check strip exists
    strip = get_strip(strip_id)
    if (strip == None):
        abort(404)
    r = request.json.get('red')
    if not (isinstance(r, int) and 0 <= r <= 255):
        abort(400)
    g = request.json.get('green')
    if not (isinstance(g, int) and 0 <= g <= 255):
        abort(400)
    b = request.json.get('blue')
    if not (isinstance(b, int) and 0 <= b <= 255):
        abort(400)
    strip.setRgb(r, g, b)
    # Return new values
    return strip.get_data_as_json()

##
# Check Auth
##
def is_auth_needed():
    return LEDnet.config.has_key("authKey")

def check_auth(json_data):
    if (LEDnet.config.has_key("authKey") and not 'authKey' in json_data):
        return False
    if (LEDnet.config.has_key("authKey") and 'authKey' in json_data and not (LEDnet.config["authKey"] == json_data.get('authKey'))):
        return False
    return True

##
# Error Handlers
##

# 400 - Bad request
@lednet.errorhandler(400)
def error_bad_request(error):
    return make_response(jsonify({'error': {'description': 'Bad request.', 'code': 400}}), 400)

# 401 - Unauthorized
@lednet.errorhandler(401)
def error_unauthorized(error):
    return make_response(jsonify({'error': {'description': 'Unauthorized.', 'code': 401}}), 401)

# 404 - Not found
@lednet.errorhandler(404)
def error_not_found(error):
    return make_response(jsonify({'error': {'description': 'Not found.', 'code': 404}}), 404)

# 405 - Method not allowed
@lednet.errorhandler(405)
def error_method_not_allowed(error):
    return make_response(jsonify({'error': {'description': 'Method not allowed.', 'code': 405}}), 405)

# 500 - Internal server error
@lednet.errorhandler(500)
def error_internal_server_error(error):
    return make_response(jsonify({'error': {'description': 'Internal server error.', 'code': 500}}), 500)

##
# Start servr
##

def start_server():
    lednet.run(host='0.0.0.0')