from abc import ABC, abstractmethod

class SiteScraper(ABC):

    @abstractmethod
    def nextListingLink(self):
        pass

    @abstractmethod
    def getListingFromListPage(self, link):
        pass
