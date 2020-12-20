from siteScraperClass import SiteScraper
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class DoItOrgScraper(SiteScraper):

    def __init__(self, browser):
        self.currentListingListPage = 1
        self.baseListingListString = "https://do-it.org/opportunities/search?page={}&miles=50"
        self.currentListingListData = []

        self.browser = browser

        self.maxWait = 20

    def findElements(self, cssSelector):
        raise NotImplementedError("This site is not implemented")
        # return WebDriverWait(self.browser, self.maxWait).until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, cssSelector))
        # )

    def nextListingLink(self):
        raise NotImplementedError("This site is not implemented")
        # while True:
        #     #if empty
        #     if len(self.currentListingListData) == 0:
        #         # get new view buttons
        #         urlToSearch = self.baseListingListString.format(self.currentListingListPage)
        #         self.browser.get(urlToSearch)
        #         #let it load
        #         newViewButtons = self.findElements("a.view")
        #         self.currentListingListData = [elem.get_attribute('href') for elem in newViewButtons]
        #
        #         self.currentListingListPage += 1
        #
        #         yield self.currentListingListData.pop()
        #     else:
        #         yield self.currentListingListData.pop()

    def getListingFromListPage(self, link):
        raise NotImplementedError("This site is not implemented")
        # self.browser.get(link)
        # print(link)
        #
        # #wait for it to load
        # newDescription = self.findElements('p[ng-bind-html="opportunity.clean_description | preserveLineBreaks"]')[0].text
        # newCharityDescription = self.findElements('p[ng-bind-html="opportunity.for_recruiter.blurb | preserveLineBreaks"]')[0].text
        # skills = self.findElements('p[ng-bind-html="opportunity.clean_blurb | preserveLineBreaks"]')[0].text
        #
        # print("newDescription")
        # print(newDescription)
        # print("newCharityDescription")
        # print(newCharityDescription)
        # print("skills")
        # print(skills)
        #
        # pass
