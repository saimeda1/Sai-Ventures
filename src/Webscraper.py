import pandas as pd
import requests
from bs4 import BeautifulSoup


#Web scraper for Nasdaq to get desired data on user desired stock and desired time period
def gatherDataNasdaq(ticker,length):
    #Initlizes the page based on user selected stock output
    page = "https://www.nasdaq.com/market-activity/stocks/"+ticker+"/historical"



def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)
        

def open_html(path):
    with open(path, 'rb') as f:
        return f.read()



