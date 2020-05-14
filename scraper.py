import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import sys

path_to_save = sys.argv[1]
pages = int(sys.argv[2])

def get_rs(url):
    rs = requests.get(url)
    soup = BeautifulSoup(rs.text, features="html.parser")
    return soup

def get_titles(soup):
    titles = [i.get_text() for i in soup.find_all("h4", {"class": 'maxarts-news-title maxarts-text-break'})]
    return titles

def get_dates_and_views(soup):
    dates_and_views = soup.find_all("span", {"class": 'maxarts-text-small'})
    dates = [i.get_text() for i in dates_and_views if "դիտում" not in i.get_text()]
    views = [i.get_text().strip().split(" ")[0] for i in dates_and_views if "դիտում" in i.get_text()]
    return dates, views

def scrape_pages(path_to_save, pages=2):
        
    data = {
        "titles": [],
        "dates": [],
        "views": []
    }
    
    for p in range(1, pages + 1):
        url = "https://m.shamshyan.com/hy/articles/all/" + str(p)
        soup = get_rs(url)
        titles = get_titles(soup)
        dates, views = get_dates_and_views(soup)
        if len(titles) == 0:
            break
        data['titles'].extend(titles)
        data['dates'].extend(dates)
        data['views'].extend(views)
        
    pd.DataFrame(data).to_csv(path_to_save + "/" + str(date.today()) + " shamsh.csv")

scrape_pages(path_to_save, pages)