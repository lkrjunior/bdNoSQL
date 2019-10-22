import configparser
import pandas as pd
from ListTweetsHandler import ListTweetsHandler
from Neo4jHandler import Neo4jHandler
from TwitterHandler import TwitterHandler
from MongoDbConnection import MongoDbConnection
from ComprehendHandler import ComprehendHandler

config = configparser.RawConfigParser()
config.read('config.properties')

section = 'DatabaseSection'
connectionString = config.get(section, 'database.connectionString')

section = 'TwitterSection'
consumerKey = config.get(section, 'twitter.consumerKey')
consumerSecret = config.get(section, 'twitter.consumerSecret')
accessToken = config.get(section, 'twitter.accessToken')
accessTokenSecret = config.get(section, 'twitter.accessTokenSecret')

mongoDbConnection = MongoDbConnection(connectionString)
twitter = TwitterHandler(consumerKey, consumerSecret, accessToken, accessTokenSecret)
listTweetsHandler = ListTweetsHandler()


deleteAllObjects = mongoDbConnection.findAll()
for doc in deleteAllObjects:
    mongoDbConnection.deleteOne(doc)
print("MongoDB clean successfuly")

resultType = "recent"
query = "bolsonaro" + " -filter:retweets"
language = "pt"
geocode = "-30.0277,-51.2287,5km"
since = "2019-01-01"
until = "2019-12-31"
numberItems = 100

cidades = pd.DataFrame(data={
        'pais':[
                'Brasil',
                'Brasil',
                'Brasil',
                'Brasil',
                'Brasil',
                'Brasil',
                'Brasil'
                ],
        'uf':[
                'MG',
                'DF',
                'PR',
                'CE',
                'RS',
                'RJ',
                'SP'
                ],
        'cidades':[
                'Belo_Horizonte',
                'Brasilia',
                'Curitiba',
                'Fortaleza',
                'Porto_Alegre',
                'Rio_de_Janeiro',
                'Sao_Paulo'
                ],
        'geo':[
                '-19.9208,-43.9378,10km',
                '-15.7797,-47.9297,10km',
                '-25.4278,-49.2731,10km',
                '-3.7172,-38.5430,10km',
                '-30.0330,-51.23,10km',
                '-22.9028,-43.2075,10km',
                '-23.5475,-46.6361,10km'
                ]
        })

listTweets = []
for index,row in cidades.iterrows():
    pais = row['pais']
    uf = row['uf']
    cidade = row['cidades']
    geo = row['geo']
    tweetsSearch = twitter.searchItems(resultType, query, language, geo, since, until, numberItems)
    for tweet in tweetsSearch:
        if tweet:
            tweetInsertion = {
                "idUser": tweet.id_str,
                "createAt": tweet.created_at.isoformat(),
                "date": tweet.created_at.strftime("%d/%m/%Y"),
                "screenName": tweet.user.screen_name,
                "tweet": tweet.text,
                "pais" : pais, 
                "uf": uf,
                "cidade":cidade,
            }
            listTweets.append(tweetInsertion)

if len(listTweets) > 0:
    mongoDbConnection.insertMany(listTweets)
    print('Sentimental Analysis on Twiteer successfuly!')

mongoDbConnection.close()
twitter.close()
comprehendHandler.close()
