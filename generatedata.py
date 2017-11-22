from urllib.request import urlopen
from lxml import html
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import traceback

class Player:
    
    BR_URL_PREFIX = "https://www.basketball-reference.com/players/"
    HTML_PARSER = "html.parser"
    FEATURE_LABEL_INDEX_MAP = { 
        'g' : 0, 
        'gs' : 1,
        'mp_per_g' : 2,
        'fg_per_g' : 3,
        'fga_per_g' : 4,
        'fg_pct' : 5,
        'fg3_per_g' : 6, 
        'fg3a_per_g' : 7,
        'fg3_pct' : 8,
        'efg_pct' : 9,
        'ft_per_g' : 10,
        'fta_per_g' : 11,
        'ft_pct' : 12,
        'pts_per_g' : 13,
        'trb_per_g' : 14,
        'ast_per_g' : 15,
        'stl_per_g' : 16,
        'blk_per_g' : 17,
        'All Star' : 18,
        'All-NBA' : 19,
        'All-Defensive' : 20,
        'NBA Scoring Champ' : 21,
        'Def. POY' : 22,
        'AS MVP' : 23,
        'Finals MVP' : 24,
        'MVP' : 25, 
        'NBA Champ' : 26 }

    # instance variables:
    #     player_name 
    #     soup
    
    def __init__(self, player_name, international, hof):
        self.player_name = player_name
        self.international = international
        self.hof = hof
        player_name = player_name.lower()
        if (len(player_name.split(" ")) != 2):
            print(player_name, "is not a valid player, player name must be in the precise format 'FIRST_NAME LAST_NAME'")
        else:
            suffix = player_name.split()[-1][0] + "/" + player_name.split()[1][:5] + player_name.split()[0][:2]  + "01.html"
            url = self.BR_URL_PREFIX + suffix
            try:
                html = urlopen(url)
                self.soup = BeautifulSoup(html, self.HTML_PARSER)
            except :
                print("Invalid URL for player:", self.player_name, " URL:", url) 

    def load_data(self):
        try:
            career_acheivements = [ s.string for s in self.soup.find('ul', id='bling').find_all("a") ]
            career_stats = [ (s.attrs['data-stat'], float(s.string.strip())) for s in self.soup.find('table').find('tfoot').find('tr').findAll('td') if is_numeric(str(s.string)) ]
        except:
            print("Could not parse data for player:", self.player_name)
            return 
        player_data = self.parse_acheivements(career_acheivements) + career_stats
        features = [0] * 28
        for (key, value) in player_data:
            if key in self.FEATURE_LABEL_INDEX_MAP:
                features[self.FEATURE_LABEL_INDEX_MAP[key]] = value
        features[-1] = float(self.international)
        feature_label_set = [features, [float(self.hof)]]
        print(self.player_name, feature_label_set)
        return feature_label_set
    
    def parse_acheivements(self, career_acheivements):
        parsed_acheivements = []
        for ca in career_acheivements:
            if ca == "Hall of Fame":
                continue
            ca = ca.split()
            if '-' in ca[0]:
                parsed_acheivements.append((" ".join(ca[1:]), 1))
            elif 'x' in ca[0]:
                parsed_acheivements.append((" ".join(ca[1:]), float(ca[0][:-1])))
            else:
                print("Cannot parse career acheivement for", self.player_name, "--", ca)
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
    training_data = []
    f = open("trainingdata.txt")
    for line in f.readlines():
        line = line.split(',')
        player = Player(line[0], line[1], line[2])
        training_data.append(player.load_data())
    f.close()

    print(len(training_data))

    print("DONE")