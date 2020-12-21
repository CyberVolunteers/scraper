from dynamicSiteScraper import DynamicSiteScraper


class DoItOrgScraper(DynamicSiteScraper):

    def __init__(self, browser, maxWait=20):
        self.currentListingListPage = 1
        self.baseListingListString = "https://do-it.org/opportunities/search?page={}&miles=50"
        super().__init__(browser, maxWait)

    def getNewLinks(self):
        # get new view buttons
        urlToSearch = self.baseListingListString.format(self.currentListingListPage)
        self.browser.get(urlToSearch)
        # let it load
        newViewButtons = self.findElements("a.view")
        self.currentListingListData = [elem.get_attribute('href') for elem in newViewButtons]

        self.currentListingListPage += 1

    def getListingFromListPage(self, link):
        self.browser.get(link)
        print(link)

        #wait for it to load
        newDescription = self.findElements('p[ng-bind-html="opportunity.clean_description | preserveLineBreaks"]')[0].text
        newCharityDescription = self.findElements('p[ng-bind-html="opportunity.for_recruiter.blurb | preserveLineBreaks"]')[0].text
        skills = self.findElements('p[ng-bind-html="opportunity.clean_blurb | preserveLineBreaks"]')[0].text

        print("newDescription")
        print(newDescription)
        print("newCharityDescription")
        print(newCharityDescription)
        print("skills")
        print(skills)

        pass
