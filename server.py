import sys
import json
import base64

import token
import urllib
import random
import requests
import argparse

from flask import Flask
from flask import jsonify
from flask import request

import pocket
from pocket import Pocket

from managers.redisAccountManager import RedisAccountManager

API_TOKEN = ""
ACCOUNTS = {}
#CLIENT_URL = 'http://5dac3c14.ngrok.com'
CLIENT_URL = 'http://415a13ef.ngrok.com'

app = Flask(__name__)
accounts = RedisAccountManager()

# Yo endpoint
@app.route('/yo/<poll>/', methods=['GET'])
def get_yo(poll):
    print poll
    username = request.args.get('username')
    link  = request.args.get('link')
    print "Usernm"
    print username
    uid = accounts.get_uid(username)
    if uid is None:
        # create new account, send pocket info
        uid = accounts.gen_uid(username) 
        print "uid generation"
        print uid
        send_link_yo(username, API_TOKEN, CLIENT_URL + "/connectPocket/" + uid) 
    else:
        # check if we have pocket secret
        secret = accounts.get_secret(uid)
        if secret is None:
            print "NO SECRET"
            print "uid being sent"
            print uid
            send_link_yo(username, API_TOKEN, CLIENT_URL + "/connectPocket/" + uid) 
        else:
            if link is None:
                send_read_link(username, uid, API_TOKEN)
            else:
                pocket_instance = pocket.Pocket(CONSUMER_KEY, secret)
                pocket_instance.add(link)
                
                print "received a link on an already existing account"

    return 'OK'

# Pocket Linking endpoint
@app.route('/linkPocket/', methods=['POST'])
def post_linkPocket():
    uid = request.headers.get('Authorization')
    content = request.get_json()
    request_token = content['code']
    if uid is None:
        print "WTF uid is none on linkPocket"

    user_credentials = Pocket.get_credentials(consumer_key=CONSUMER_KEY, code=request_token)
    secret = user_credentials['access_token']
    accounts.set_secret(uid, secret)
    return 'OK'

# Link read endpoint
@app.route('/readLink/', methods=['POST'])
def post_readLink():
    uid = request.headers.get('Authorization')
    content = request.get_json()
    item_id = content["item_id"]

    # archive the link!
    access_token = accounts.get_secret(uid) 
    print "a t"
    print access_token
    pocket_instance = pocket.Pocket(CONSUMER_KEY, access_token)
    pocket_instance.archive(item_id, wait=False)
     
    return "OK"


def send_link_yo(username, api_token, link):
    requests.post("http://api.justyo.co/yo/", data={'api_token': api_token, 'username': username, 'link': link})

def send_read_link(username, uid, api_token):
    # api call
    print "sending read link!"
    access_token = accounts.get_secret(uid) 
    pocket_instance = pocket.Pocket(CONSUMER_KEY, access_token)
    response = pocket_instance.get()[0]
    unread = response['list'].keys()
    random_pick = unread[random.randrange(len(unread))]
    url = response['list'][random_pick]['given_url']
    
    r = {}
    r['item_id'] = random_pick
    r['aid'] = uid
    r['url'] = url
    kek = urllib.urlencode(r)
    send_link_yo(username, API_TOKEN, CLIENT_URL + "/reader?" + kek)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launch the Kenobi backend server")
    parser.add_argument('-c', '--consumer-key', help='the Kenobi pocket cons key', required=True)
    parser.add_argument('-k', '--api-key', help='the Yo api key')
    args = parser.parse_args(sys.argv[1:])

    CONSUMER_KEY = args.consumer_key
    API_TOKEN = args.api_key

    app.run(debug=True)
