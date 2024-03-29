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

section = 'Neo4jSection'
connectionStringNeo4j = config.get(section, 'neo4j.connectionString')
userNeo4j = config.get(section, 'neo4j.user')
passwordNeo4j = config.get(section, 'neo4j.password')

section = 'ComprehendSection'
accessKeyComprehend = config.get(section, 'comprehend.accessKey')
secretAccessKeyComprehend = config.get(section, 'comprehend.secretAccessKey')

mongoDbConnection = MongoDbConnection(connectionString)
twitter = TwitterHandler(consumerKey, consumerSecret, accessToken, accessTokenSecret)
neo4j = Neo4jHandler(connectionStringNeo4j, userNeo4j, passwordNeo4j)
comprehendHandler = ComprehendHandler(accessKeyComprehend, secretAccessKeyComprehend)
listTweetsHandler = ListTweetsHandler()


deleteAllObjects = mongoDbConnection.findAll()
for doc in deleteAllObjects:
    mongoDbConnection.deleteOne(doc)
print("MongoDB clean successfuly")

listSentimentals = {
    "POSITIVE": 0,
    "NEGATIVE": 0,
    "NEUTRAL": 0,
    "MIXED": 0
}



resultType = "recent"
query = "bolsonaro" + " -filter:retweets"
language = "pt"
geocode = "-30.0277,-51.2287,5km"
since = "2019-01-01"
until = "2019-12-31"
numberItems = 5

cidades = pd.DataFrame(data={
        'cidades':[
                'Belo_Horizonte_MG',
                'Brasilia_DF',
                'Curitiba_PR',
                'Fortaleza_CE',
                'Porto_Alegre_RS',
                'Rio_de_Janeiro_RJ',
                'Sao_Paulo_SP'
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
    cidade = row['cidades']
    geo = row['geo']
    tweetsSearch = twitter.searchItems(resultType, query, language, geo, since, until, numberItems)
    for tweet in tweetsSearch:
        if tweet:
            comprehendAnalysis = comprehendHandler.detectSentiment(tweet.text)
            sentiment = comprehendAnalysis['Sentiment']
            tweetInsertion = {
                "idUser": tweet.id_str,
                "createAt": tweet.created_at.isoformat(),
                "date": tweet.created_at.strftime("%d/%m/%Y"),
                "screenName": tweet.user.screen_name,
                "location": cidade,
                "tweet": tweet.text,
                "cidade":cidade,
                "sentimental": sentiment
            }
            listTweets.append(tweetInsertion)
            #tweetInsertion['location'] = listTweetsHandler.onlyCharacters(tweetInsertion['location'])
            tweetSentimental = {'location': tweetInsertion['location'], 'sentimental': tweetInsertion['sentimental']}
            listTweets.append(tweetSentimental)
            print("Tweet to send MongoDB: " + str(tweetSentimental))

listRelations = listTweetsHandler.analyseDataSentimental(listTweets)
listRelationsPercentage = listTweetsHandler.calculatePercentage(listRelations)

neo4j.clean()
neo4j.insertSentimentals(listSentimentals)
neo4j.insertLocations(listRelationsPercentage)
neo4j.insertRelations(listRelationsPercentage)
print("Neo4J inserted successfuly!")



if len(listTweets) > 0:
    mongoDbConnection.insertMany(listTweets)
    print('Sentimental Analysis on Twiteer successfuly!')

mongoDbConnection.close()
twitter.close()
neo4j.close()
comprehendHandler.close()
