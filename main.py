from selenium import webdriver

baseUrlsListingList = ["https://do-it.org/opportunities/search"]
isDynamic = [True]
baseUrlsIndividualListings = [""]

# page = requests.get(baseUrlsListingList[0])
#
# print(page.content)
#
# parsedHTML = BeautifulSoup(page.content, 'html.parser')
#
# print(parsedHTML)

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

browser = webdriver.Firefox(r"C:\Program Files\geckodriver")

from siteScraperFunctions.doItOrg import DoItOrgScraper
from siteScraperFunctions.bhCommunityWorks import BHCommunityWorksScraper

scraper = BHCommunityWorksScraper(browser)

nextListingLinkGen = scraper.nextListingLink()

while True:
    try:
        link = next(nextListingLinkGen)
    except RuntimeError:
        print("End")
        break
    data = scraper.getListingFromListPage(link)

    import pprint
    pprint.PrettyPrinter(indent=4).pprint(data)
