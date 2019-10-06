import pymongo
from INoSqlConnection import INoSqlConnection


class MongoDbConnection(INoSqlConnection):
    def __init__(self, connectionString):
        self.client = pymongo.MongoClient(connectionString)
        self.db = self.client.nosql

    def findOne(self, findOne):
        findObject = self.db.nosql.find_one(findOne)
        return findObject

    def findAll(self):
        findObjects = self.db.nosql.find()
        return findObjects

    def insertOne(self, insertOne):
        id = self.db.nosql.insert_one(insertOne)
        return id.inserted_id

    def insertMany(self, insertMany):
        ids = self.db.nosql.insert_many(insertMany)
        return ids.inserted_ids

    def deleteOne(self, deleteOne):
        self.db.nosql.delete_one(deleteOne)

    def close(self):
        self.client.close()
