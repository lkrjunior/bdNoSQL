from abc import abstractmethod


class INoSqlConnection:
    @abstractmethod
    def findOne(self, findOne):
        raise NotImplementedError

    @abstractmethod
    def insertOne(self, insertOne):
        raise NotImplementedError

    @abstractmethod
    def deleteOne(self, deleteOne):
        raise NotImplementedError
