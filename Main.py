import configparser
from MongoDbConnection import MongoDbConnection

config = configparser.RawConfigParser()
config.read('config.properties')
connectionString = config.get('DatabaseSection', 'database.connectionString')
print(connectionString)

mongoDbConnection = MongoDbConnection(connectionString)

insertOne = {"_id": 1, "name": "nosql", "teste": "1"}
mongoDbConnection.insertOne(insertOne)

objectId = {"_id": 1}
mongoDbConnection.findOne(objectId)

mongoDbConnection.deleteOne(objectId)