from .context import tweetqueue
from datetime import datetime, timedelta
import pytest
from tweetqueue import user

from replit import db


user_data = {
        'access_token_key': 'test_access_token',
        'access_token_secret': 'test secret',
        'id': '3213213123',
        'name': 'Chris Behan',
        'tweets': ['Carpe diem', 'hello world'],
        'cadence': 1,
        'last_tweet': str(datetime.now())
        }
def test_create():
    test_user = user.User(**user_data)
    assert test_user
    assert test_user.access_token_key == user_data['access_token_key']

def test_serialize_deserialize():
    test_user = user.User(**user_data)
    assert test_user.name == user_data['name']
    user_str = test_user.serialze()
    new_user = user.User.deserialize(user_str)
    # assert dict representation of user is the staticmethod after serialize/deserialize
    assert new_user.dict() == test_user.dict()

def test_save_user(): 
    test_user = user.User(**user_data)
    db[test_user.id] = test_user.serialze()
    loaded_user_data = db[test_user.id]
    loaded_user = user.User.deserialize(loaded_user_data)
    assert test_user.dict() == loaded_user.dict()
    # Clean up test db
    del db[test_user.id]

def test_next_tweet():
    test_user = user.User(**user_data)
    first_in_tweet = test_user.tweets[-1]
    next_tweet = test_user.pop_tweet()
    assert next_tweet == first_in_tweet

def test_add_tweet():
    test_user = user.User(**user_data)
    tweet = "test tweet"
    test_user.add_tweet(tweet)
    assert test_user.tweets[0] == tweet

def test_tweet_interval():
    test_user = user.User(**user_data)
    interval = timedelta(hours=24 // test_user.cadence)
    assert test_user.tweet_interval() == interval

def test_time_to_tweet_true():
    test_user = user.User(**user_data)
    interval = test_user.tweet_interval()
    now = datetime.now()
    test_user.last_tweet = now - interval
    assert test_user.should_tweet(now) == True

def test_time_to_tweet_false():
    test_user = user.User(**user_data)
    interval = test_user.tweet_interval()
    interval -= timedelta(minutes=1)
    now = datetime.now()
    test_user.last_tweet = now - interval
    assert test_user.should_tweet(now) == False

    
