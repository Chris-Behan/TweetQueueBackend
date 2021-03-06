import os
import json
from TwitterAPI import TwitterAPI
import requests
from urllib.parse import parse_qs
from requests_oauthlib import OAuth1
from tweetqueue.user import User
from typing import Dict
from replit import db

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token_key = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
user_api = TwitterAPI(consumer_key, consumer_secret, access_token_key,
                      access_token_secret)

callback_uri = 'https://tweetqueue.behan.repl.co/queue.html'
request_key = None
request_secret = None


def login():
    oauth_token, oauth_token_secret = get_oauth_tokens()
    twitter_sign_in_link = generate_sign_in_link(oauth_token)
    return twitter_sign_in_link, 200


def get_oauth_tokens():
    oauth = OAuth1(consumer_key, consumer_secret, callback_uri=callback_uri)
    res = requests.post(url='https://api.twitter.com/oauth/request_token',
                        auth=oauth)
    if res.status_code != 200:
        raise Exception('Unexpected response from /oauth/request_token')
    content = res.content.decode('utf-8')
    credentials = parse_qs(content)
    callback_confirmed = credentials['oauth_callback_confirmed'][0]
    if callback_confirmed != 'true':
        raise Exception('Callback url is not confirmed!')
    oauth_token = credentials['oauth_token'][0]
    oauth_token_secret = credentials['oauth_token_secret'][0]
    return oauth_token, oauth_token_secret


def generate_sign_in_link(token: str):
    sign_in_link = f'https://api.twitter.com/oauth/authenticate?oauth_token={token}'
    return sign_in_link


def get_user(verifier: str, oauth_token: str):
    credentials = get_credentials(verifier, oauth_token)
    access_token_key = credentials.get('oauth_token')
    access_token_secret = credentials.get('oauth_token_secret')
    user_info = get_user_info(access_token_key, access_token_secret)
    if(user_info['id'] in db):
        user_str: str = db[user_info['id']]
        user: User = User.deserialize(user_str)
        user.name = user_info['name']
        user.id = user_info['id']
        return user
    else:
        user_dict = {
        'access_token_key': access_token_key,
        'access_token_secret': access_token_secret,
        'id': user_info['id'],
        'name': user_info['name']
        }
        user = User(**user_dict)
    save_user(user)
    return user



def get_credentials(verifier: str, oauth_token: str) -> Dict[str, str]:
    oauth = OAuth1(consumer_key,
                   consumer_secret,
                   resource_owner_key=oauth_token,
                   verifier=verifier)

    response = requests.post(url='https://api.twitter.com/oauth/access_token',
                             auth=oauth)
    # response is in bytes, decode to utf-8 string
    content = response.content.decode('utf-8')
    credentials = parse_qs(content)
    # credentials dict is in form {str: List[str]} where List[str] has 1 element.
    # Transform to {str: str}
    return {key: value[0] for (key, value) in credentials.items()}


def get_user_info(key: str, secret: str):
    api = TwitterAPI(consumer_key, consumer_secret, key, secret)
    res = api.request('account/verify_credentials')
    res_dict = json.loads(res.text)
    print(res_dict)
    return res_dict


def save_user(user: User):
    db[user.id] = user.serialze()


def tweet(text: str, user: User, test: bool = False):
    if test:
        print(f'Pretending to tweet: {test}')
        return
    api = TwitterAPI(consumer_key, consumer_secret, user.access_token_key,
                     user.access_token_secret)
    r = api.request('statuses/update', {'status': text})
    print(r.status_code)

def add_tweet(user: User, text: str):
    user.add_tweet(text)

