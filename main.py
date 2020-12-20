from siteScraperFunctions.doItOrg import *
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

baseUrlsListingList = ["https://do-it.org/opportunities/search"]
isDynamic = [True]
baseUrlsIndividualListings = [""]
page = requests.get(baseUrlsListingList[0])

print(page.content)

parsedHTML = BeautifulSoup(page.content, 'html.parser')

print(parsedHTML)


browser = webdriver.Firefox(r"C:\Program Files\geckodriver")
# browser.get('http://seleniumhq.org/')

# binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
# browser = webdriver.Firefox(firefox_binary=binary, executable_path=r"C:\Program Files\geckodriver")
# browser.get('https://stackoverflow.com')

from siteScraperFunctions.doItOrg import DoItOrgScraper

scraper = DoItOrgScraper(browser)

nextListingLinkGen = scraper.nextListingLink()

for i in range(15):
    link = next(nextListingLinkGen)
    scraper.getListingFromListPage(link)
