import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_clubs_from_search(url: str) -> pd.DataFrame:
    """Find the table that contains clubs, get the names, urls and countries"""
    headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    tables = pageSoup.find_all("div", {"class": "large-12 columns"})

    clubs = []
    country_flags = []
    for table in tables:
        if 'Search results: Clubs' in table.text:
            clubs = table.find_all('td', {'class':'hauptlink'})
            country_flags = table.find_all('img', {'class':'flaggenrahmen'})

    club_names = []
    country_names = []
    urls = []
    for i in range(len(clubs)):
        club_names.append(clubs[i].text.strip())
        country_names.append(country_flags[i].attrs.get('title').strip())
        urls.append(f"https://www.transfermarkt.com{clubs[i].find_all('a')[0].attrs.get('href').strip()}")

    clubs_scrape_df = pd.DataFrame({"club_names":club_names,"country_names":country_names, "urls": urls})

    return clubs_scrape_df



def get_players_from_search(url: str) -> pd.DataFrame:
    """Need to find a div with class='table-header' with text 'SEARCH RESULTS FOR PLAYERS' """
    headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    players = pageSoup.find_all("", {"class": ""})


def club_info(url: str) -> pd.DataFrame: 
    """Extracting the data from a club page.
    Here we are looking for the total MV, top arrivals and top departures"""


    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
 
    mv = pageSoup.find_all("div", {"class": "dataMarktwert"})[0].text.strip()

    top_departures = pageSoup.find_all("div", {"data-viewport":"TopTransfers_abgaenge"})[0] 
    top_departures_names = top_departures.find_all('table')[0].find_all('span', {'class' : 'spielername'})
    top_departures_fee = top_departures.find_all('table')[0].find_all('td', {'class' : 'rechts'})
    top_departures_to = top_departures.find_all('table')[0].find_all('span', {'class' : 'wappen-ab'})

    departed = []
    earned = []
    left_to = []
    for i in range(len(top_departures_names)):
        departed.append(top_departures_names[i].text.strip())
        earned.append(top_departures_fee[i].text.strip())
        left_to.append(top_departures_to[i].img.attrs.get("title").strip())

    departures_df = pd.DataFrame({"player":departed,"fee":earned, "left to": left_to})


    top_arrivals = pageSoup.find_all("div", {"data-viewport":"TopTransfers_zugaenge"})[0]
    top_arrivals_names = top_arrivals.find_all('table')[0].find_all('span', {'class' : 'spielername'})
    top_arrivals_fee = top_arrivals.find_all('table')[0].find_all('td', {'class' : 'rechts'})
    top_arrivals_from = top_arrivals.find_all('table')[0].find_all('span', {'class' : 'wappen-ab'})


    arrived = []
    paid = []
    arrived_from = []
    for i in range(len(top_arrivals_names)):
        arrived.append(top_arrivals_names[i].text.strip())
        paid.append(top_arrivals_fee[i].text.strip())
        arrived_from.append(top_arrivals_from[i].img.attrs.get("title").strip())
    

    arrivals_df = pd.DataFrame({"player":arrived,"fee":paid, "arrived from": arrived_from})

    return departures_df, arrivals_df, mv


