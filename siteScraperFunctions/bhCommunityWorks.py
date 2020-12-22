from dynamicSiteScraper import DynamicSiteScraper
import pprint

pp = pprint.PrettyPrinter(indent=4)

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
        # print(link)
        print(len(self.currentListingListData))
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

        categoryNames = ["", "Skills", "Benefits", "Practical Considerations", "When do I need to be available?", "Where does this role take place?"]
        dictNames = ["opportunityDesc", "skills", "opportunityDesc", "opportunityDesc", "timeForVolunteering", "placeForVolunteering"]
        indices = [overallText.find(name) for name in categoryNames] + [len(overallText) - len("Register your Interest")]

        out = {}

        # print(categoryNames)
        # print(indices)

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

            if newDictName in out:
                out[newDictName] += "\n<b>" + newCategoryName + "</b>\n" + newText
            else:
                out[newDictName] = newText
            out[newDictName] = out[newDictName].replace("\n", "<br/>")

            # print(newCategoryName, newDictName)
            # print(indices[0] + len(newCategoryName), indices[1])

            indices.pop(0)

        out["opportunityTitle"] = self.findElements(".mb-2")[0].text
        out["numOfvolunteers"] = -1
        out["minHoursPerWeek"] = -1
        out["maxHoursPerWeek"] = -1
        out["charityId"] = 0

        if "timeForVolunteering" in out:
            index = out["timeForVolunteering"].find("Morning Afternoon Evening")
            out["timeForVolunteering"] = out["timeForVolunteering"][:index]

        # fill in the remaining fields
        linkToSiteHtml = '<a class="moreDetails" href="%s">More Details</a>' % link
        for requiredField in allFields:
            if requiredField not in out:
                out[requiredField] = linkToSiteHtml

        # pp.pprint(out)

        out["opportunityDesc"] += "\n" + linkToSiteHtml + "\n"

        return out

