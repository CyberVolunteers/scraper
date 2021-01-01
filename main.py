import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import sql

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

options = Options()
options.add_argument("--headless")

browser = webdriver.Firefox(firefox_profile=r"C:\Program Files\geckodriver", options=options)

from siteScraperFunctions.bhCommunityWorks import BHCommunityWorksScraper

scraper = BHCommunityWorksScraper(browser)

nextListingLinkGen = scraper.nextListingLink()


def scrape():
    # add the new ones
    while True:
        try:
            link = next(nextListingLinkGen)
        except RuntimeError:
            print("End")
            break
        data = scraper.getListingFromListPage(link)

        import pprint

        pprint.PrettyPrinter(indent=4).pprint(data)

        data["uuid"] = sql.generate_uuid()
        data["createdDate"] = int(time.time())
        data["opportunityCategory"] = "Not available"
        print(time.time())

        listingObject = sql.ListingsTable(**data)
        sql.recordInDb(listingObject, data)

    browser.quit()


def update():
    # delete the old ones
    sql.deleteFromSite("https://volunteer.bhcommunityworks.org.uk/")

    # add the new ones
    scrape()


update()
