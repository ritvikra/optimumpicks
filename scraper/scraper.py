from bs4 import BeautifulSoup
import requests
import pandas as pd

import pandas as pd
from datetime import date
from pymongo import MongoClient



def clean_odds(odd):
    # Replace non-standard hyphen with standard hyphen
    return odd.replace('−', '-')

def draftkingsML():
    moneylines = pd.DataFrame(columns=['game_id','team_away', 'team_home','dk_away_odds','dk_home_odds'])
    url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
    req = requests.get(url)
    soup = BeautifulSoup(req.content,"html.parser")
    f = open('moneylines.txt', 'w')
    tables = soup.find_all('tbody')
    for table in tables:
        rows = table.find_all('tr')
        for i in range(0, len(rows)):
            find_teamName = rows[i].find('div', class_='event-cell__name-text')
            if i == 0:
                find_opp = rows[1].find('div', class_='event-cell__name-text')
                oppOddsRow = rows[1].find_all('td')[-1]
                oppOdds = oppOddsRow.find('span')
                oppOdds = int(clean_odds(oppOdds.text.strip()))
            elif i == 1:
                find_opp = rows[0].find('div', class_='event-cell__name-text')
                oppOddsRow = rows[0].find_all('td')[-1]
                oppOdds = oppOddsRow.find('span')
                oppOdds = int(clean_odds(oppOdds.text.strip()))
            elif i % 2 == 0 and i < len(rows) - 1: 
                find_opp = rows[i+1].find('div', class_='event-cell__name-text') 
                oppOddsRow = rows[i + 1].find_all('td')[-1]
                oppOdds = oppOddsRow.find('span')
                oppOdds = int(clean_odds(oppOdds.text.strip()))
            elif i:
                find_opp = rows[i - 1].find('div', class_='event-cell__name-text')
                oppOddsRow = rows[i - 1].find_all('td')[-1]
                oppOdds = oppOddsRow.find('span')
                oppOdds = int(clean_odds(oppOdds.text.strip()))
            if i % 2 == 0:
                if find_teamName:
                    teamName = find_teamName.text.strip()
                    oppName = find_opp.text.strip()
                    game_id = '' + teamName + oppName + str(date.today())
                    moneylineRow = rows[i].find_all('td')[-1]
                    
                    if moneylineRow:
                        mlOddbool = moneylineRow.find('span')
                        if mlOddbool:
                            mlOdd = int(clean_odds(mlOddbool.text.strip()))
                            moneylines.loc[len(moneylines.index)] = [game_id, teamName, oppName, mlOdd, oppOdds]
                            f.write(f"Away: {teamName}, Home: {oppName}, Moneyline Odds for Away: {mlOdd}, MoneyLine Odds for Home: {oppOdds}\n")

    moneylines.to_csv('/Users/ritvikrallapalli/ritvikra/OptimumPicks/scraper/moneylines.csv', index=False)

def main():
    draftkingsML()