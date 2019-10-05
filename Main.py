import configparser

from TwitterHandler import TwitterHandler
from MongoDbConnection import MongoDbConnection

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
    print("Location for delete: " + doc['user']['location'])
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

twitter = TwitterHandler(consumerKey, consumerSecret, accessToken, accessTokenSecret)
query = 'BigDataAnalytics'
twitters = twitter.search(query)
for tweet in twitters:
    #print(f' Usuário: {tweet.user} - Tweet: {tweet.text}')
    locationFromTweet = tweet._json['user']['location']
    if locationFromTweet.strip():
        print("Location: " + tweet._json['user']['location'])
        mongoDbConnection.insertOne(tweet._json)

print("Tweets inserted succeed")


