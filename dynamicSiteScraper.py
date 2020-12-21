from abc import abstractmethod
from siteScraperClass import SiteScraper

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class DynamicSiteScraper(SiteScraper):

    def __init__(self, browser, maxWait):
        self.currentListingListData = []

        self.browser = browser

        self.maxWait = maxWait

    def findElements(self, cssSelector):
        return WebDriverWait(self.browser, self.maxWait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, cssSelector))
        )

    @abstractmethod
    def getNewLinks(self):
        pass

    def nextListingLink(self):
        while True:
            if len(self.currentListingListData) == 0:
                self.getNewLinks()
            yield self.currentListingListData.pop()

    @abstractmethod
    def getListingFromListPage(self, link):
        pass
