from flask import Flask
from flask_cors import CORS
from flask import request
import tweet

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return "hello world!"

@app.route('/tweet', methods=['POST'])
def tweet_handler():
  data = request.json
  if 'text' not in data:
    return "Expected 'text' to be in body of request", 400

  print(data)
  tweet.tweet('hello')
  return "received!"
  
app.run(host='0.0.0.0', port=8080)
