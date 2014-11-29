import sys
import json

import requests
import argparse

from flask import Flask
from flask import jsonify
from flask import request

API_TOKEN = ""
ACCOUNTS = {}
CLIENT_URL = 'http://5dac3c14.ngrok.com'

app = Flask(__name__)

# Yo endpoint
@app.route('/yo/<poll>/', methods=['GET'])
def get_yo(poll):
    print poll
    username = request.args.get('username')

    # TODO: send random link to user
    
    return 'OK'

# Create new user 
@app.route('/create/<username>/', methods=['POST'])
def post_create(uid):
    api_key = json.loads(request.data)

    return 'OK'

def return_status(status, message):
    result = {}
    result['result'] = status 
    result['message'] = message
    return jsonify(result)

def send_link_yo(username, api_token, link):
    requests.post("http://api.justyo.co/yo/", data={'api_token': api_token, 'username': username, 'link': link})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launch the Kenobi backend server")
    parser.add_argument('-k', '--api-key', help='the Kenobi keys file', required=True)
    args = parser.parse_args(sys.argv[1:])

    API_TOKEN = args.api_key

    app.run(debug=True)
