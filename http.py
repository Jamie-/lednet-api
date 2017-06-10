from flask import Flask, abort, request, make_response, jsonify
from strip import Strip
import time
import json

lednet = Flask(__name__)

##
# Endpoints
##

@lednet.route('/', methods=['GET'])
def get_index():
    return jsonify({"systemName": config["systemName"]})

@lednet.route('/info', methods=['GET'])
def get_info():
    return jsonify({"system": {"systemName": config["systemName"], "systemTime": time.strftime("%H:%M.%S"), "strips": config["stripQty"], "cycle": "day"}})

@lednet.route('/config', methods=['GET', 'POST'])
def get_config():
    if (request.method == 'GET'):
        abort(401)
    if not (request.json):
        abort(400)
    if not (check_auth(request.json)):
        abort(401)
    return json.dumps(config)

# See system LED data
@lednet.route('/led', methods=['GET'])
def get_led_data():
    return jsonify({"strips": {"qty": config["stripQty"]}})

# View strip output data
@lednet.route('/led/<int:strip_id>', methods=['GET'])
def get_strip_values(strip_id):
    if (strip_id >= len(strips)):
        abort(404)
    s = strips[strip_id]
    return jsonify({'strip': {'red': s.getR(), 'green': s.getG(), 'blue': s.getB(), 'mode': s.get_mode()}})

@lednet.route('/led/<int:strip_id>', methods=['POST'])
def set_strip_rgb(strip_id):
    # Check request is JSON
    if not (request.json):
        abort(400)
    # Check for authentication
    if not (check_auth(request.json)):
        abort(401)
    # Update strips
    s = strips[strip_id]
    r = request.json.get('r')
    if not (isinstance(r, int) and 0 <= r <= 255):
        abort(400)
    g = request.json.get('g')
    if not (isinstance(g, int) and 0 <= g <= 255):
        abort(400)
    b = request.json.get('b')
    if not (isinstance(b, int) and 0 <= b <= 255):
        abort(400)
    s.setRgb(r, g, b)
    # Return new values
    return jsonify({'strip': {'red': s.getR(), 'green': s.getG(), 'blue': s.getB(), 'mode': s.get_mode()}})

##
# Check Auth
##
def check_auth(json_data):
    if (config.has_key("authKey") and not 'authKey' in json_data):
        return False
    if (config.has_key("authKey") and 'authKey' in json_data and not (config["authKey"] == json_data.get('authKey'))):
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