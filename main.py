# Webscrape Creditex
import requests
from bs4 import BeautifulSoup
import pandas
import os
import shutil
import pathlib



session = requests.Session()  # persist parameters and cookies
years0 = range(2005,2007)
years1 = range(2006, 2008)
years3 = range(2010, 2023)
#
main_url = 'https://www.creditfixings.com{id}'
urlyears1 = 'https://www.creditfixings.com/CreditEventAuctions/static/credit_event_auction/{year}.shtml'
url2008id = 'https://www.creditfixings.com/CreditEventAuctions/static/credit_event_auction/2008/{id}'
url2009id = 'https://www.creditfixings.com/CreditEventAuctions/static/credit_event_auction/{id}'
urlyears3 = 'https://www.creditfixings.com/CreditEventAuctions/AuctionByYear.jsp?year={year}'
urlid = 'https://www.creditfixings.com/CreditEventAuctions/{id}'

path_output_csv = os.getcwd()+"/Output_csv"

path_output_jpg = os.getcwd()+"/Output_jpg"

pathlib.Path(path_output_csv).mkdir(parents=True, exist_ok=True)



def reqpars_y(source, year):
    html = session.get(source.format(year=year)).text  # request the html by year
    soup = BeautifulSoup(html, "html.parser")
    return soup

def reqpars_id(source, id):
    html = session.get(source.format(id=id)).text  # request the html by year
    soup = BeautifulSoup(html, "html.parser")
    return soup


for year in years0:
    auctionIds = reqpars_y(urlyears1, year).find_all("span", class_="standalonelink")  # import all the anchor that have "holdings.jsp" in their href
    length = len(auctionIds)  # how many auction for each year
    i: int
    for i in range(length):
        id = auctionIds[i].find('a')['href']  # now let's extract the link to each auction
        soup = reqpars_id(main_url,id)  # parse the html
        ticker = id.split(str(year)+"/",1)[1][:-6]
        print(auctionIds[i].text)
        for idx, img in enumerate(soup.select('img[src^="/information/affiliations/fixings/20"]')) :  # add the name of the company whose CDS are auctioned before each table
            sc = requests.get(main_url.format(id=img['src']),stream = True)
            table_title = img.find_previous('h2').text
            if sc.status_code == 200:
                with open(path_output_jpg + "/" + str(year) + " " + ticker + " " + str(idx) + " " + str(table_title)[0:34] + ".jpg",'wb') as f:
                    shutil.copyfileobj(sc.raw, f)


for year in years1:
    auctionIds = reqpars_y(urlyears1, year).find_all("span", class_="standalonelink")  # import all the anchor that have "holdings.jsp" in their href
    length = len(auctionIds)  # how many auction for each year
    i: int
    for i in range(length):
        id = auctionIds[i].find('a')['href']  # now let's extract the link to each auction
        soup = reqpars_id(main_url,id)  # parse the html
        ticker = id.split(str(year)+"/",1)[1][:-6]
        print(auctionIds[i].text)
        for idx, table in enumerate(soup.find_all('table')):  # add the name of the company whose CDS are auctioned before each table
            temp = pandas.read_html(str(table))  # print all the table
            df = pandas.DataFrame(temp[0])  # title = str(year)+ " " +auction_name+str(idx)+".csv"
            table_title = table.find_previous('h2').text
            df.to_csv(path_output_csv + "/" + str(year) + " " + ticker + " " + str(idx) + " " + str(table_title)[0:34] + ".csv",index=False)

year = 2008
auctionIds = reqpars_y(urlyears1, year).find_all("span", class_="standalonelink")  # import all the anchor that have "holdings.jsp" in their href
length = len(auctionIds)  # how many auction for each year
i: int
for i in range(length):
    id1 = auctionIds[i].find('a')['href']  # now let's extract the link to each auction
    results = reqpars_id(main_url,id1).find_all("span", class_="standalonelink")[0]
    id2 = results.find('a')['href'].replace("dis", "res")
    soup3 = reqpars_id(url2008id,id2.split(str(year) + "/", 1)[-1])
    ticker = id2.split(str(year) + "/", 1)[-1][:-10]
    print(auctionIds[i].text)
    for idx, table in enumerate(soup3.find_all('table')):  # add the name of the company whose CDS are auctioned before each table
        temp = pandas.read_html(str(table))  # print all the table
        df = pandas.DataFrame(temp[0])  # title = str(year)+ " " +auction_name+str(idx)+".csv"
        table_title = table.find_previous('h2').text
        df.to_csv(path_output_csv + "/" + str(year) + " " + ticker + " " + str(idx) + " " + str(table_title)[0:34] + ".csv",index=False)


year = 2009
auctionIds = reqpars_y(urlyears1, year).find_all("span", class_="standalonelink")  # import all the anchor that have "holdings.jsp" in their href
length = len(auctionIds)  # how many auction for each year
i: int
for i in range(length):
    id1 = auctionIds[i].find('a')['href']  # now let's extract the link to each auction
    auction_name = auctionIds[i].text
    id2 = id1.replace("index", "results")
    soup2 = reqpars_id(url2009id, id2)
    print(auction_name)
    auction_name = id2.split(str(year) + "/", 1)[1][:-14]
    for idx, table in enumerate(soup2.find_all('table')):
        temp = pandas.read_html(str(table))
        if temp == []: #SSP had zero NOI so there was an empty table
            continue
        df = pandas.DataFrame(temp[0])  # title = str(year)+ " " +auction_name+str(idx)+".csv"
        table_title = table.find_previous('h2').text
        df.to_csv(path_output_csv + "/" + str(year) + " " + auction_name + " " + str(idx) + " " + str(table_title)[0:34] + ".csv",index=False)

year = 2010
auctionIds = reqpars_y(urlyears3, year).select( 'a[href^="/information/affiliations/fixings/20"]')  # import all the anchor that have "holdings.jsp" in their href
length = len(auctionIds)  # how many auction for each year
# auctionIds = reqpars_y(urlyears3, year).find_all("span", class_="standalonelink")  # it does not work with standalone when you try to get href
for i in range(length):
    id1 = auctionIds[i].get('href')  # now let's extract the link to each auction
    auction_name = auctionIds[i].text
    soup2 = reqpars_id(main_url, id1)  # parse the html
    id2 = id1.replace("index", "results")
    soup3 = reqpars_id(main_url, id2)  # parse the page
    print(auction_name)
    auction_name = id2.split(str(year) + "/", 1)[1][:-14]
    for idx, table in enumerate(soup3.find_all('table')):
        temp = pandas.read_html(str(table))
        if temp == []: #McCarthy had zero NOI so there was an empty table
            continue
        df = pandas.DataFrame(temp[0])  # title = str(year)+ " " +auction_name+str(idx)+".csv"
        table_title = table.find_previous('h2').text
        df.to_csv(path_output_csv + "/" + str(year) + " " + auction_name + " " + str(idx) + " " + str(table_title)[0:34] + ".csv",index=False)

for year in years3:
    auctionIds = reqpars_y(urlyears3, year).select('a[href^="holdings.jsp"]')  # import all the anchor that have "holdings.jsp" in their href
    length = len(auctionIds)  # how many auction for each year
    for i in range(length):
        id1 = auctionIds[i].get('href')  # now let's extract the link to each auction
        ticker = reqpars_id(urlid, id1).select('a[href^="results.jsp"]')  # select the anchor that have results.jsp in href
        if ticker == []: #McCarthy had zero NOI so there was an empty table
            continue
        id2 = ticker[0].get('href')  # it extracts something like "/results.jsp?ticker=ASTL"
        soup3 = reqpars_id(urlid, id2)  # parse the page
        print(ticker[0].text)
        auction_name = id2.replace('results.jsp?ticker=', '')
        for idx, table in enumerate(soup3.find_all('table')):
            temp = pandas.read_html(str(table))  # print all the table
            df = pandas.DataFrame(temp[0])  # title = str(year)+ " " +auction_name+str(idx)+".csv"
            table_title = table.find_previous('h2').text
            df.to_csv(path_output_csv + "/" + str(year) + " " + auction_name + " " + str(idx) + " " + str(table_title)[0:34] + ".csv", index=False)

