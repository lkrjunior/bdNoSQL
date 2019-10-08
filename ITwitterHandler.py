from abc import abstractmethod


class ITwitterHandler:
    @abstractmethod
    def search(self, query):
        raise NotImplementedError

    @abstractmethod
    def searchItems(self, resultType, query, language, geocode, since, until, numberItems):
        raise NotImplementedError