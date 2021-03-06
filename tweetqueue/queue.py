import threading
from replit import db
from tweetqueue.user import User
from tweetqueue.tweet import tweet
from datetime import datetime

class QueueThread:
    def __init__(self):
        self.queue = threading.Thread()

    def start(self):
        self.queue = threading.Timer(5, self.work)
        self.queue.start()

    def work(self):
        print('doing work')
        user_ids = db.keys()
        for id in user_ids:
            # Load user from db
            user_str = db[id]
            user = User.deserialize(user_str)
            print(user.name)
            # get current time
            now = datetime.now()

            if user.should_tweet(now): 
                if user.has_tweet():
                    tweet_content = user.pop_tweet()
                    tweet(tweet_content, user)
                    user.last_tweet = now
                    # serialize and save user to db
                    user_str = user.serialze()
                    db[id] = user_str

        self.queue = threading.Timer(5, self.work)
        self.queue.start()