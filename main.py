from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
from tweetqueue import tweet
import time
import threading

app = Flask(__name__)
CORS(app)

q_thread = threading.Thread()

@app.route('/')
def index():
    return "hello world!"


@app.route('/login')
def login_handler():
    return tweet.login()


@app.route('/getUser', methods=['POST'])
def get_user_handler():
    body = request.json
    oauth_verifier = body['oauth_verifier']
    oauth_token = body['oauth_token']
    user = tweet.get_user(oauth_verifier, oauth_token)
    return jsonify(**user.dict())

@app.route('/tweet', methods=['POST'])
def tweet_handler():
    data = request.json
    if 'text' not in data:
        return "Expected 'text' to be in body of request", 400

    print(data)
    tweet.tweet('hello')
    return "received!"

def queue_handler():
    global q_thread
    q_thread = threading.Timer(1, parse_queue, ())
    q_thread.start()

def parse_queue():
    global q_thread
    print('hello from thread')
    q_thread = threading.Timer(1, parse_queue, ())
    q_thread.start()
    

queue_handler()
app.run(host='0.0.0.0', port=8080)
