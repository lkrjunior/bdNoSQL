import tweepy
from ITwitterHandler import ITwitterHandler


class TwitterHandler(ITwitterHandler):
    def __init__(self, consumerKey, consumerSecret, accessToken, accessTokenSecret):
        authentication = tweepy.OAuthHandler(consumerKey, consumerSecret)
        authentication.set_access_token(accessToken, accessTokenSecret)
        self.twitter = tweepy.API(authentication)

    def search(self, query):
        resultQuery = self.twitter.search(q=query)
        return resultQuery