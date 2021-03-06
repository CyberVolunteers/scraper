from dynamicSiteScraper import DynamicSiteScraper


class BHCommunityWorksScraper(DynamicSiteScraper):

    def __init__(self, browser, maxWait=20):
        self.baseListingListString = "https://volunteer.bhcommunityworks.org.uk/"
        self.newLinksAvaliable = True
        super().__init__(browser, maxWait)

    def getNewLinks(self):
        if not self.newLinksAvaliable:
            raise RuntimeError("The site does not have more links to consider")

        # get new view buttons
        self.browser.get(self.baseListingListString)
        # let it load
        listButton = self.findElements("#list-tab")

        # go to the list view
        listButton[0].click()

        cardTitles = self.findElements("div.card.mb-4 > .card-body > .card-title > a")

        self.currentListingListData = [elem.get_attribute("href") for elem in cardTitles]

        self.newLinksAvaliable = False

    def getListingFromListPage(self, link):
        self.browser.get(link)

        """
        Required format:

        {
            timeForVolunteering:
            placeForVolunteering:
            targetAudience:
            skills:
            createdDate:
            requirements:
            opportunityDesc:
            opportunityCategory:
            opportunityTitle:
            numOfvolunteers:
            minHoursPerWeek:
            maxHoursPerWeek:
            duration:
            charityId:    
        }

        """

        mainBody = self.findElements(".pr-4")[0]
        overallText = mainBody.text

        allFields = ["timeForVolunteering",
                     "placeForVolunteering",
                     "targetAudience",
                     "skills",
                     "requirements",
                     "opportunityDesc",
                     "duration"]

        categoryNames = ["", "Skills", "Benefits", "Practical Considerations", "When do I need to be available?",
                         "Where does this role take place?"]
        dictNames = ["opportunityDesc", "skills", "opportunityDesc", ["opportunityDesc", "requirements"],
                     "timeForVolunteering", "placeForVolunteering"]
        indices = [overallText.find(name) for name in categoryNames] + [
            len(overallText) - len("Register your Interest")]

        out = {}

        while len(categoryNames) != 0:
            # if it is skipped, pop
            if indices[1] == -1:
                # skip
                indices.pop(1)
                categoryNames.pop(1)
                dictNames.pop(1)
            newCategoryName = categoryNames.pop(0)
            newDictName = dictNames.pop(0)
            newText = overallText[indices[0] + len(newCategoryName): indices[1]]

            if isinstance(newDictName, str):
                newDictNames = [newDictName]
            else:
                newDictNames = newDictName

            for newKey in newDictNames:
                if newKey in out:
                    out[newKey] += "\n<b>" + newCategoryName + "</b>\n" + newText
                else:
                    out[newKey] = newText
                out[newKey] = out[newKey].replace("\n", "<br/>")

            indices.pop(0)

        out["opportunityTitle"] = self.findElements(".mb-2")[0].text
        out["scrapedCharityName"] = self.findElements(".opportunity-header .container h3.mb-4")[0].text
        out["numOfvolunteers"] = -1
        out["minHoursPerWeek"] = -1
        out["maxHoursPerWeek"] = -1
        out["charityId"] = 0

        if "timeForVolunteering" in out:
            index = out["timeForVolunteering"].find("Morning Afternoon Evening")
            out["timeForVolunteering"] = out["timeForVolunteering"][len("<br/>Details "):index]

        # fill in the remaining fields
        linkToSiteHtml = '<a class="moreDetails" href="%s">More Details</a>' % link
        for requiredField in allFields:
            if requiredField not in out:
                out[requiredField] = linkToSiteHtml

        out["opportunityDesc"] += "\n" + linkToSiteHtml + "\n"

        return out
