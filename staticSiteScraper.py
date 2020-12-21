from abc import abstractmethod
from siteScraperClass import SiteScraper


class StaticSiteScraper(SiteScraper):

    @abstractmethod
    def nextListingLink(self):
        pass

    @abstractmethod
    def getListingFromListPage(self, link):
        pass
