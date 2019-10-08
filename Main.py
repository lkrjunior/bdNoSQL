#pip3 freeze
#criar arquivo requirements.txt com as bilbiotecas 
#pip3 install -r requirements.txt

import configparser

from Neo4jHandler import Neo4jHandler
from TwitterHandler import TwitterHandler
from MongoDbConnection import MongoDbConnection
from ComprehendHandler import ComprehendHandler

config = configparser.RawConfigParser()
config.read('config.properties')

section = 'DatabaseSection'
connectionString = config.get(section, 'database.connectionString')
print("database.connectionString: " + connectionString)

section = 'TwitterSection'
consumerKey = config.get(section, 'twitter.consumerKey')
consumerSecret = config.get(section, 'twitter.consumerSecret')
accessToken = config.get(section, 'twitter.accessToken')
accessTokenSecret = config.get(section, 'twitter.accessTokenSecret')
print("twitter.consumerKey: " + consumerKey)
print("twitter.consumerSecret: " + consumerSecret)
print("twitter.accessToken: " + accessToken)
print("twitter.accessTokenSecret: " + accessTokenSecret)



mongoDbConnection = MongoDbConnection(connectionString)

deleteAllObjects = mongoDbConnection.findAll()
for doc in deleteAllObjects:
    #if 'user' in doc or 'tweet' in doc:
        #print("Location for delete: " + doc['user']['location'])
        mongoDbConnection.deleteOne(doc)
print("All documents on db nosql deleted succeed")

insertOne = {"_id": 1, "name": "nosql", "teste": "1"}
id = mongoDbConnection.insertOne(insertOne)
print("insertOne: _id=" + str(id) + " inserted")

objectId = {"_id": 1}
result = mongoDbConnection.findOne(objectId)
print("findOne: " + str(result))

mongoDbConnection.deleteOne(objectId)
print("deleteOne: " + str(objectId) + " deleted")

insertMany = [
    {"_id": 1, "name": "nosql1", "teste": "1"},
    {"_id": 2, "name": "nosql2", "teste": "2"}
]
ids = mongoDbConnection.insertMany(insertMany)
print("insertMany: _ids=" + str(ids) + " inserted")

for idToDelete in ids:
    deleteOne = {"_id": idToDelete}
    mongoDbConnection.deleteOne(deleteOne)
print("deleteMany: " + str(ids) + " deleted")

twitter = TwitterHandler(consumerKey, consumerSecret, accessToken, accessTokenSecret)
query = 'BigDataAnalytics'
twitters = twitter.search(query)
for tweet in twitters:
    #print(f' User: {tweet.user} - Tweet: {tweet.text}')
    locationFromTweet = tweet._json['user']['location']
    if locationFromTweet.strip():
        print("Location: " + tweet._json['user']['location'])
        tweetUser = tweet._json['user']
        tweetInsertion = {
            "idUser": tweetUser['id'], 
            "name": tweetUser['name'], 
            "screenName": tweetUser['screen_name'], 
            "location": tweetUser['location'], 
            "tweet": tweetUser['description']
            }
        mongoDbConnection.insertOne(tweetInsertion)

print("Tweets inserted succeed")

mongoDbConnection.close()


section = 'Neo4jSection'
connectionStringNeo4j = config.get(section, 'neo4j.connectionString')
userNeo4j = config.get(section, 'neo4j.user')
passwordNeo4j = config.get(section, 'neo4j.password')

neo4j = Neo4jHandler(connectionStringNeo4j, userNeo4j, passwordNeo4j)
neo4j.createMessage("message to test")
print("Neo4j inserted succeed")

neo4j.close()


section = 'ComprehendSection'
accessKeyComprehend = config.get(section, 'comprehend.accessKey')
secretAccessKeyComprehend = config.get(section, 'comprehend.secretAccessKey')

comprehendHandler = ComprehendHandler(accessKeyComprehend, secretAccessKeyComprehend)
comprehendSentiment = comprehendHandler.detectSentiment('twitter é tri')
print (comprehendSentiment)