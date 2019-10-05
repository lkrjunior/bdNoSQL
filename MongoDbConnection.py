import pymongo

from INoSqlConnection import INoSqlConnection


class MongoDbConnection(INoSqlConnection):
    def __init__(self, connectionString):
        client = pymongo.MongoClient(connectionString)
        self.db = client.nosql

    def findOne(self, findOne):
        findObject = self.db.nosql.find_one(findOne)
        print("findOne: " + str(findObject))

    def insertOne(self, insertOne):
        id = self.db.nosql.insert_one(insertOne)
        print("insertOne: Id=" + str(id.inserted_id) + " inserted")

    def deleteOne(self, deleteOne):
        self.db.nosql.delete_one(deleteOne)
        print("deleteOne: " + str(deleteOne) + " deleted")