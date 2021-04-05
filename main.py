import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import bs4
import requests
from datetime import datetime
from pathlib import Path


def handle_line(condamne, columns):
    column = 0
    for element in condamne:
        if not isinstance(element, bs4.element.NavigableString):
            if element.get_text() == 'Last Statement' or element.get_text() == 'Inmate Information':
                try:
                    print(element.a['href'])
                    columns[column].append(element.a['href'])
                except Exception:
                    print('error')
            else:
                print(element.get_text())
                columns[column].append(element.get_text())
            column = column+1
            
def get_lastwords(urls, lastwordslist):
    for url in  urls: 
        url_complete = 'https://www.tdcj.texas.gov/death_row/' + url
        req_condamne = requests.get(url_complete)
        soup_condamne = BeautifulSoup(req_condamne.text, "lxml")
        condamnes_discours = soup_condamne.find_all('p')
        discours = ''
        to_add = False
        for element in condamnes_discours:
            if to_add:
                discours = discours + element.get_text()
            if 'Last Statement:' in element.get_text():
                to_add= True
        lastwordslist.append(discours)


def __main__():
    req = requests.get('https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html')
    soup = BeautifulSoup(req.text, "lxml")
    condamnes = soup.find_all('tr')
    columns= [list() for _ in  range(11)]
    
    for condamne in condamnes[1,:]:
        handle_line(condamne, columns)

    get_lastwords(columns[2], columns[10])
        
        
    d = {
        'id': columns[0],
        'inmate_info_link': columns[1],
	'lastwords_info_link':columns[2],
        'lastname': columns[3],
        'fistname': columns[4],
        'TDCJ': columns[5],
        'age': columns[6],
        'date': columns[7],
        'race': columns[8],
        'country': columns[9],
        'lastwords': columns[10]
    }

    df = pd.DataFrame(data=d)

    df.to_csv('deathrow_text.csv')

    
