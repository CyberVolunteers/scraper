import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from siteScraperFunctions.bhCommunityWorks import BHCommunityWorksScraper

import sql

from sys import argv

import builtins

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

logFile = open("./scraper.log", "a")


def logPrint(fun):
    def onPrint(*args, **kwargs):
        fun(*args, **kwargs)
        logFile.write(repr(args) + " " + repr(kwargs) + "\n")

    return onPrint


@logPrint
def print(*args, **kwargs):
    return builtins.print(*args, **kwargs)


def scrape(credentials, scraper, nextListingLinkGen):
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
        sql.recordInDb(listingObject, data, credentials)


def update(credentials, scraper, nextListingLinkGen):
    # delete the old ones
    sql.deleteFromSite("https://volunteer.bhcommunityworks.org.uk/", credentials)

    # add the new ones
    scrape(credentials, scraper, nextListingLinkGen)


if __name__ == '__main__':
    print("---Start Log---")
    if len(argv) != 4:
        print("Wrong number of arguments, expected 4")
        raise Exception("Wrong number of arguments, expected 4, received these arguments: ", argv)

    print("Retrieving credentials")
    credentials = (argv[1], argv[2])
    period = int(argv[3])

    print("Time period: ", period)

    # browser
    print("Setting up the browser")
    options = Options()
    options.add_argument("--headless")
    if os.name == "nt": # win
        browser = webdriver.Firefox(options=options)
    else: # linux
        browser = webdriver.Firefox(executable_path="/home/mikhail/cybervolunteers/drivers/geckodriver", options=options)

    # scraper
    print("Setting up the scrapers")
    scraper = BHCommunityWorksScraper(browser)
    nextListingLinkGen = scraper.nextListingLink()

    try:
        while True:
            update(credentials, scraper, nextListingLinkGen)
            time.sleep(period)
    except Exception as e:
        print("Exception")
        print(e)
        browser.quit()
