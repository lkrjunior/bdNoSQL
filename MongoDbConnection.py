import pymongo
from INoSqlConnection import INoSqlConnection


class MongoDbConnection(INoSqlConnection):
    def __init__(self, connectionString):
        client = pymongo.MongoClient(connectionString)
        self.db = client.nosql

    def findOne(self, findOne):
        findObject = self.db.nosql.find_one(findOne)
        return findObject

    def findAll(self):
        findObjects = self.db.nosql.find()
        return findObjects

    def insertOne(self, insertOne):
        id = self.db.nosql.insert_one(insertOne)
        return id.inserted_id

    def deleteOne(self, deleteOne):
        self.db.nosql.delete_one(deleteOne)