import os
from TwitterAPI import TwitterAPI
import requests
from urllib.parse import parse_qs
from requests_oauthlib import OAuth1
from user import User
from typing import Dict

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


def get_user(verifier:str, oauth_token:str):
    credentials = get_credentials(verifier, oauth_token)
    access_token_key = credentials.get('oauth_token')
    access_token_secret = credentials.get('oauth_token_secret')
    user_id = credentials.get('user_id')
    screen_name = credentials.get('screen_name')
    return User(access_token_key, access_token_secret, user_id, screen_name)


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
    return {key:value[0] for (key, value) in credentials.items()}
