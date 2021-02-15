import json
from datetime import datetime, timedelta


class User:
    def __init__(self, **kwargs):
        self.access_token_key = kwargs.get('access_token_key')
        self.access_token_secret = kwargs.get('access_token_secret')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.tweets = kwargs.get('tweets')
        self.cadence = kwargs.get('cadence')
        self.last_tweet = kwargs.get('last_tweet')

    def dict(self):
        return {
        'access_token_key': self.access_token_key,
        'access_token_secret': self.access_token_secret,
        'id': self.id,
        'name': self.name,
        'tweets': self.tweets,
        'cadence': self.cadence,
        'last_tweet': self.last_tweet
        }

    def serialze(self):
        return json.dumps(self.dict())
    
    @staticmethod
    def deserialize(data: str):
        user_data : dict = json.loads(data)
        return User(**user_data)

    def pop_tweet(self):
        return self.tweets.pop()

    def add_tweet(self, tweet):
        self.tweets.insert(0, tweet)

    def tweet_interval(self) -> timedelta:
        return timedelta(hours=24//self.cadence)

    def should_tweet(self, t: datetime):
        return t >= self.last_tweet + self.tweet_interval()
        
    def set_last_tweet_time(self, t: datetime):
        self.last_tweet = t
