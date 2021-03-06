from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from tweetqueue import tweet
from tweetqueue import queue
from flask import g
import time
import threading
from replit import db

app = Flask(__name__)
CORS(app, supports_credentials=True)

q_thread = threading.Thread()

@app.before_request
def extract_access_token():
    access_token_key = request.cookies.get('access_token_key')
    access_token_secret = request.cookies.get('access_token_secret')
    user_id = request.cookies.get('user_id')
    if access_token_key and access_token_secret:
        g.access_token_key = access_token_key
        g.access_token_secret = access_token_secret
        g.user_id = user_id
        print('tokens set')


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
    response = make_response(jsonify(**user.dict()), 200)
    access_token_key, access_token_secret = user.get_credentials()
    response.set_cookie('hello', 'world')
    response.set_cookie('access_token_key', access_token_key, httponly=True)
    response.set_cookie('access_token_secret', access_token_secret, httponly=True)
    return response

@app.route('/tweet', methods=['POST'])
def tweet_handler():
    print('credentials in cookies:')
    hello_cookie = request.cookies.get('hello')
    print(hello_cookie)
    print(request.cookies.get('hello'))
    print(request.cookies.get('access_token_key'))
    print(request.cookies.get('access_token_secret'))
    data = request.json
    if 'text' not in data:
        return "Expected 'text' to be in body of request", 400

    print(data)
    response = make_response()
    # tweet.tweet('hello')
    return response


@app.route('/tweets', methods=['POST', 'GET'])
def tweets_handler():
    if request.method == 'POST':
        print('add tweet to queue')
        print(g.access_token_key)
        print(g.access_token_secret)
        data = request.json
        if 'text' not in data:
            return "Expected 'text' to be in body of request", 400
        tweet: str = data['text'] 
        



# def queue_handler():
#     global q_thread
#     q_thread = threading.Timer(1, parse_queue, ())
#     q_thread.start()

# def parse_queue():
#     global q_thread
#     print('hello from thread')
#     q_thread = threading.Timer(1, parse_queue, ())
#     q_thread.start()
    
q = queue.QueueThread()
q.start()

app.run(host='0.0.0.0', port=8080)
