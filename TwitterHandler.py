import tweepy
from ITwitterHandler import ITwitterHandler


class TwitterHandler(ITwitterHandler):
    def __init__(self, consumerKey, consumerSecret, accessToken, accessTokenSecret):
        authentication = tweepy.OAuthHandler(consumerKey, consumerSecret)
        authentication.set_access_token(accessToken, accessTokenSecret)
        self.twitter = tweepy.API(authentication)
        self.twitterApi = tweepy

    def search(self, query):
        resultQuery = self.twitter.search(q=query)
        return resultQuery

    def searchItems(self, resultType, query, language, geocode, since, until, numberItems):
        #tweets = self.twitter.search(result_type=resultType,
        #                             q=query,
        #                             lang=language,
        #                             geocode=geocode,
        #                             since=since,
        #                             until=until).items(numberItems)
        tweets = self.twitterApi.Cursor(self.twitter.search,
                                        result_type=resultType,
                                        q=query,
                                        lang=language,
                                        geocode=geocode,
                                        since=since,
                                        until=until).items(numberItems)
        return tweets

    def close(self):
        self.twitter = None
        self.twitterApi = None
