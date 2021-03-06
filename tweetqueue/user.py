import json
from datetime import datetime, timedelta
from typing import Tuple

class User:
    def __init__(self, **kwargs):
        self.access_token_key = kwargs.get('access_token_key')
        self.access_token_secret = kwargs.get('access_token_secret')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.tweets = kwargs.get('tweets', [])
        self.cadence = kwargs.get('cadence', 1)
        self.last_tweet = kwargs.get('last_tweet', datetime(2021, 1, 1, 1, 1))

    def dict(self):
        return {
            'access_token_key': self.access_token_key,
            'access_token_secret': self.access_token_secret,
            'id': self.id,
            'name': self.name,
            'tweets': self.tweets,
            'cadence': self.cadence,
            'last_tweet': str(self.last_tweet)
        }

    def get_credentials(self) -> Tuple:
        return self.access_token_key, self.access_token_secret
        

    def serialze(self):
        return json.dumps(self.dict())

    @staticmethod
    def deserialize(data: str):
        user_data: dict = json.loads(data)
        user_data['last_tweet'] = datetime.fromisoformat(
            user_data['last_tweet'])
        return User(**user_data)

    def pop_tweet(self):
        return self.tweets.pop()

    def has_tweet(self):
        return self.tweets

    def add_tweet(self, tweet):
        self.tweets.insert(0, tweet)

    def tweet_interval(self) -> timedelta:
        return timedelta(hours=24 // self.cadence)

    def should_tweet(self, t: datetime):
        return t >= self.last_tweet + self.tweet_interval()

    def set_last_tweet_time(self, t: datetime):
        self.last_tweet = t
