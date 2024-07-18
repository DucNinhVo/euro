from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import urllib.parse
import re
import pandas as pd

def player_data(url):
    player_html = urlopen(url, context=ctx).read()
    player_soup = BeautifulSoup(player_html, "html.parser")

    player_tables = player_soup.find_all('table')
    player_table = player_tables[0].find('tbody').find_all('tr')
   
    player_info = []
    for row in player_table:
        if row.find('th'):
            row_header = row.find('th').get_text(strip=True).lower()
            if row_header == 'date of birth':
                birth_date = row.find('td').get_text(strip= True)[1:11]
                player_info.append(birth_date)
            if row_header == 'place of birth':
                birth_place = re.sub(r'\[\d+\]','',row.find('td').get_text(strip= True)) 
                player_info.append(birth_place)
            if row_header == 'height':
                height = float(row.find('td').get_text(strip= True)[:4]) * 100
                player_info.append(height)
            if row_header == 'current team':
                club = row.find('td').get_text(strip= True)
                player_info.append(club)
    return player_info    
            
def match_data(url, table_nr,team):
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the table tags, table 11 has the info i need 
    tables = soup('table')

    # table 11 has the info for the match Ger - Den 
    # inside table 11 there are 2 sub-table 12 and 13 for Ger and Den 
    # the data i need is inside a 'tr' tag nested in 'tbody'
    # dont need the first row and last row
    players = tables[table_nr].find('tbody').find_all('tr')[1:-1]

    player_list = []
    for player in players:    
        cols = player.find_all('td')    
        if len(cols) >= 3:
            posistion = cols[0].get_text(strip=True)
            numb = int(cols[1].get_text(strip=True))
            link = base_url + cols[2].find('a').get('href')
            name = cols[2].find('a').get('title')
            
            player_info = [posistion,numb,link,name,team] + player_data(link)
            player_list.append(player_info)
    return player_list

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = "https://en.wikipedia.org"
url = "https://en.wikipedia.org/wiki/UEFA_Euro_2024_knockout_stage"
ger = match_data(url,12,'GER')
den = match_data(url,13,'DEN')

df = pd.DataFrame(ger + den, columns = ['postion','number','link','name','team','date_of_birth','place_of_birth','height','club'])    

df.to_csv('players.csv',index=False)
print("Data saved to players.csv")
