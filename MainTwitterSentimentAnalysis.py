import configparser
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


deleteAllObjects = mongoDbConnection.findAll()
for doc in deleteAllObjects:
    mongoDbConnection.deleteOne(doc)
print("MongoDB clean successfuly")



listTweets = []

resultType = "recent"
query = "internacional" + " -filter:retweets"
language = "pt"
geocode = "-30.0277,-51.2287,5km"
since = "2019-10-01"
until = "2019-10-09"
numberItems = 5

tweetsSearch = twitter.searchItems(resultType, query, language, geocode, since, until, numberItems)
for tweet in tweetsSearch:
    if tweet:
        #TO DO COMPREHEND
        #KEY_NOT_WORKING comprehendAnalysis = comprehendHandler.detectSentiment(tweet.text)
        #KEY_NOT_WORKING sentiment = comprehendAnalysis['Sentiment']
        sentiment = 'Neutral'
        tweetInsertion = {
            "idUser": tweet.id_str,
            "createAt": tweet.created_at,
            "screenName": tweet.user.screen_name,
            "location": tweet.user.location,
            "tweet": tweet.text,
            "sentimental": sentiment
        }
        listTweets.append(tweetInsertion)
        print("Tweet to send MongoDB: " + str(tweetInsertion))

if len(listTweets) > 0:
    mongoDbConnection.insertMany(listTweets)
    print('Sentimental Analysis on Twiteer successfuly!')

mongoDbConnection.close()
twitter.close()
neo4j.close()
comprehendHandler.close()
