# Webscrape Creditex

import requests
from bs4 import BeautifulSoup
import pandas

session = requests.Session() #persist parameters and cookiesx
years1 = range(2006, 2008)
years2 = range(2008, 2010)
years3 = range(2011, 2012)
#
main_url = 'https://www.creditfixings.com{id}'
urlyears1 = 'https://www.creditfixings.com/CreditEventAuctions/static/credit_event_auction/{year}.shtml'
url2008id = 'https://www.creditfixings.com/CreditEventAuctions/static/credit_event_auction/2008/{id}'
url2009id = 'https://www.creditfixings.com/CreditEventAuctions/static/credit_event_auction/{id}'
urlyears3 = 'https://www.creditfixings.com/CreditEventAuctions/AuctionByYear.jsp?year={year}'
urlid = 'https://www.creditfixings.com/CreditEventAuctions/{id}'

for year in years1:
    html1 = session.get(urlyears1.format(year=year)).text #request the html by year
    soup1 = BeautifulSoup(html1, "html.parser") #parse the html
    auctionId = soup1.find_all("span", class_="standalonelink") # import all the anchor that have "holdings.jsp" in their href
    length = len(auctionId)  # how many auction for each year
    for i in range(length):
        id1 = auctionId[i].find('a')['href'] # now let's extract the link to each auction
        auction_name = auctionId[i].text
        html2 = session.get(main_url.format(id=id1)).text # this the auction page and we need to select the link the bring us to the results
        soup2 = BeautifulSoup(html2, "html.parser") #parse the html
        for table in soup2.find_all('table'):
            print(auction_name)
            print(pandas.read_html(str(table)))

year = 2008
html1 = session.get(urlyears1.format(year=year)).text #request the html by year
soup1 = BeautifulSoup(html1, "html.parser")#parse the html
auctionId = soup1.find_all("span", class_="standalonelink") # import all the anchor that have "holdings.jsp" in their href
length = len(auctionId)  # how many auction for each year
for i in range(length):
    id1 = auctionId[i].find('a')['href'] # now let's extract the link to each auction
    auction_name = auctionId[i].text
    html2 = session.get(main_url.format(id=id1)).text # this the auction page and we need to select the link the bring us to the results
    soup2 = BeautifulSoup(html2, "html.parser")  #parse the html
    results = soup2.find_all("span", class_="standalonelink")[0]
    id2 = results.find('a')['href']
    id2 = id2.replace("dis", "res")
    html3 = session.get(url2008id.format(id=id2)).text # this the auction page and we need to select the link the bring us to the results
    soup3 = BeautifulSoup(html3, "html.parser")

    for table in soup3.find_all('table'):
        print(auction_name)
        print(pandas.read_html(str(table)))

year = 2009

html1 = session.get(urlyears1.format(year=year)).text #request the html by year
soup1 = BeautifulSoup(html1, "html.parser")#parse the html
auctionId = soup1.find_all("span", class_="standalonelink") # import all the anchor that have "holdings.jsp" in their href
length = len(auctionId)  # how many auction for each year
for i in range(length):
    id1 = auctionId[i].find('a')['href'] # now let's extract the link to each auction
    auction_name = auctionId[i].text
    id2 = id1.replace("index", "results")
    html2 = session.get(url2009id.format(id=id2)).text # this the auction page and we need to select the link the bring us to the results
    soup2 = BeautifulSoup(html2, "html.parser") 
     #parse the html
    for table in soup2.find_all('table'):
        print(auction_name)
        print(pandas.read_html(str(table)))

year = 2010
html1 = session.get(urlyears3.format(year=year)).text #request the html by year
soup1 = BeautifulSoup(html1, "html.parser") #parse the html
auctionId = soup1.select('a[href^="/information/affiliations/fixings/20"]')# import all the anchor that have "holdings.jsp" in their href
length = len(auctionId)  # how many auction for each year
for i in range(length):
    id1 = auctionId[i].get('href') # now let's extract the link to each auction
    auction_name = auctionId[i].text
    html2 = session.get(main_url.format(id=id1)).text # this the auction page and we need to select the link the bring us to the results
    soup2 = BeautifulSoup(html2, "html.parser") #parse the html
    id2 = id1.replace("index", "results")
    html3 = session.get(main_url.format(id=id2)).text #get to the page with results for each ticker
    soup3 = BeautifulSoup(html3, "html.parser") #parse the page
    for table in soup3.find_all('table'):
        print(auction_name)  #add the name of the company whose CDS are auctioned before each table
        print(pandas.read_html(str(table))) # print all the table


for year in years3:
    html1 = session.get(urlyears3.format(year=year)).text #request the html by year
    soup1 = BeautifulSoup(html1, "html.parser") #parse the html
    auctionId = soup1.select('a[href^="holdings.jsp"]') # import all the anchor that have "holdings.jsp" in their href
    length = len(auctionId)  # how many auction for each year
    for i in range(length):
        id1 = auctionId[i].get('href') # now let's extract the link to each auction
        auction_name = auctionId[i].text
        html2 = session.get(urlid.format(id=id1)).text # this the auction page and we need to select the link the bring us to the results
        soup2 = BeautifulSoup(html2, "html.parser") #parse the html
        ticker = soup2.select('a[href^="results.jsp"]') # select the anchor that have results.jsp in href
        id2 = ticker[0].get('href') #it extracts something like "/results.jsp?ticker=ASTL"
        html3 = session.get(urlid.format(id=id2)).text #get to the page with results for each ticker
        soup3 = BeautifulSoup(html3, "html.parser") #parse the page
        for table in soup3.find_all('table'):
            print(auction_name)  #add the name of the company whose CDS are auctioned before each table
            print(pandas.read_html(str(table))) # print all the table


#