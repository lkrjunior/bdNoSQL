import configparser

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

listTweets = []

resultType = "recent"
query = "bolsonaro" + " -filter:retweets"
language = "pt"
geocode = "-30.0277,-51.2287,5km"
since = "2019-01-01"
until = "2019-12-31"
numberItems = 20

tweetsSearch = twitter.searchItems(resultType, query, language, since, until, numberItems)
for tweet in tweetsSearch:
    if tweet:
        comprehendAnalysis = comprehendHandler.detectSentiment(tweet.text)
        sentiment = comprehendAnalysis['Sentiment']
        tweetInsertion = {
            "idUser": tweet.id_str,
            "createAt": tweet.created_at,
            "screenName": tweet.user.screen_name,
            "location": tweet.user.location,
            "tweet": tweet.text,
            "sentimental": sentiment
        }
        tweetInsertion['location'] = listTweetsHandler.onlyCharacters(tweetInsertion['location'])
        if tweetInsertion['location'].strip():
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
