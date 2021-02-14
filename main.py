from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
import tweet

app = Flask(__name__)
CORS(app)


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


    

app.run(host='0.0.0.0', port=8080)
