from urllib.request import urlopen
from lxml import html
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

class Player:
    
    BR_URL_PREFIX = "https://www.basketball-reference.com/players/"
    HTML_PARSER = "html.parser"

    
    
    def __init__(self, player_name):
        player_name = player_name.lower()
        if (len(player_name.split(" ")) != 2):
            print(player_name, "is not a valid player, player name must be in the precise format 'FIRST_NAME LAST_NAME'")
        else:
            suffix = player_name[0] + "/" + player_name.split(' ')[1][:5] + player_name.split(' ')[0][:2]  + ".html"
            self.soup = BeautifulSoup(BR_URL_PREFIX + suffix, HTML_PARSER)
            load_data()
    
    def load_data():
        career_pergame = [s.string for s in soup.find_all('tfoot')[0].find_all('td')]

alpha = "abcdefghijklmnopqrstuvwxyz"

def is_numeric(s):
    if len(s.strip()) == 0:
        return False
    for ch in alpha:
        if ch in s.strip().lower():
            return False
    return True

if __name__ == '__main__':
    f = open("testhtml.txt", 'wb')
    url = "https://www.basketball-reference.com/players/b/bryanko01.html"
    html = urlopen(url)
    bs = BeautifulSoup(html, "html5lib")
    f.write(bs.prettify().encode('utf-8'))
    f.close()

    career_acheivements = [ s.string for s in bs.find('ul', id='bling').find_all("a") ]
    print(career_acheivements)

    career_stats = [ (s.attrs['data-stat'], float(s.string.strip())) for s in bs.find('table').find('tfoot').findAll('td') if is_numeric(str(s.string)) ]

    print(career_stats)


    print("DONE")