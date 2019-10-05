from abc import abstractmethod


class ITwitterHandler:
    @abstractmethod
    def search(self, query):
        raise NotImplementedError