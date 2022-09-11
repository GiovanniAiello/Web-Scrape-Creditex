# Webscrape Creditex

import requests
from bs4 import BeautifulSoup
import pandas

session = requests.Session() #persist parameters and cookiesx
years1 = range(2005, 2010)
years2 = range(2010, 2022)
#

urlyears = 'https://www.creditfixings.com/CreditEventAuctions/AuctionByYear.jsp?year={year}'
urlid = 'https://www.creditfixings.com/CreditEventAuctions/{id}'


for year in years2:
    html1 = session.get(urlyears.format(year=year)).text #request the html by year
    soup1 = BeautifulSoup(html1, "html.parser") #parse the html
    auctionId = soup1.select('a[href^="holdings.jsp"]') # import all the anchor that have "holdings.jsp" in their href
    length = len(auctionId)  # how many auction for each year
    for i in range(length):
        id1 = auctionId[i].get('href') # now let's extract the link to each auction
        auction_name = auctionId[i].text
        html2 = session.get(urlid.format(id=id1)).text # this the auction page and we need to select the link the bring us to the results
        soup2 = BeautifulSoup(html2, "html.parser") #parse the html
        ticker = soup2.select('a[href^="results.jsp"]')
        id2 = ticker[0].get('href')
        html3 = session.get(urlid.format(id=id2)).text
        soup3 = BeautifulSoup(html3, "html.parser")
        for table in soup3.find_all('table'):
            print(auction_name)
            print(pandas.read_html(str(table)))


