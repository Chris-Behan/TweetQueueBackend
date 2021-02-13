import os
from TwitterAPI import TwitterAPI

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token_key = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)


def tweet(text: str):
  print(f'You tweeted: {text}')

def test(text):
  res = api.request('statuses/update', {'status': text})
  print(res.status_code) 