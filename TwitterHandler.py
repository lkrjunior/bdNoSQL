import tweepy
from ITwitterHandler import ITwitterHandler


class TwitterHandler(ITwitterHandler):
    def __init__(self, consumerKey, consumerSecret, accessToken, accessTokenSecret):
        autenticacao = tweepy.OAuthHandler(consumerKey, consumerSecret)
        autenticacao.set_access_token(accessToken, accessTokenSecret)
        self.twitter = tweepy.API(autenticacao)

    def search(self, query):
        resultados = self.twitter.search(q=query)
        return resultados