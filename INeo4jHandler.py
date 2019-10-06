from abc import abstractmethod


class INeo4jHandler:

    @abstractmethod
    def createMessage(self, message):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError