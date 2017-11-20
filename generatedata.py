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

    # instance variables:
    #     player_name 
    #     soup
    
    def __init__(self, player_name):
        self.player_name = player_name
        player_name = player_name.lower()
        if (len(player_name.split(" ")) != 2):
            print(player_name, "is not a valid player, player name must be in the precise format 'FIRST_NAME LAST_NAME'")
        else:
            suffix = player_name.split()[-1][0] + "/" + player_name.split()[1][:5] + player_name.split()[0][:2]  + "01.html"
            url = self.BR_URL_PREFIX + suffix
            try:
                html = urlopen(url)
                self.soup = BeautifulSoup(html, self.HTML_PARSER)
                self.load_data()
            except :
                print("Invalid URL for player:", self.player_name, " URL:", url)   

    def load_data(self):
        career_acheivements = [ s.string for s in self.soup.find('ul', id='bling').find_all("a") ]
        print(self.parse_acheivements(career_acheivements))

        career_stats = [ (s.attrs['data-stat'], float(s.string.strip())) for s in self.soup.find('table').find('tfoot').findAll('td') if is_numeric(str(s.string)) ]

        print(career_stats)
    
    def parse_acheivements(self, career_acheivements):
        parsed_acheivements = []
        for ca in career_acheivements:
            ca = ca.split()
            if '-' in ca[0]:
                parsed_acheivements.append((" ".join(ca[1:]), 1))
            elif 'x' in ca[0]:
                parsed_acheivements.append((" ".join(ca[1:]), float(ca[0][:-1])))
            else:
                print("Cannot parse career acheivement for", player_name, "--", ca)
        return parsed_acheivements



alpha = "abcdefghijklmnopqrstuvwxyz"

def is_numeric(s):
    if len(s.strip()) == 0:
        return False
    for ch in alpha:
        if ch in s.strip().lower():
            return False
    return True

if __name__ == '__main__':
    player = Player("Kobe Bryant")


    print("DONE")