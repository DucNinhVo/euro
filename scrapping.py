from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import urllib.parse

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = "https://en.wikipedia.org"
url = "https://en.wikipedia.org/wiki/UEFA_Euro_2024_knockout_stage"
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the table tags, table 11 has the info i need 
# inside table 11 there are 2 table 12 and 13 for Ger and Den 
tables = soup('table')

# content of the table is inside a 'tr' tag nested in 'tbody'
# dont need the first row
ger = tables[12].find('tbody').find_all('tr')[1:]

# get data from Ger team
for player in ger:    
    info = player.find_all('td')
    # print(info[:5])

    for cell in info:
        link_tag = cell.find('a')
        if link_tag and link_tag.get('href'):
            player_link = base_url + urllib.parse.unquote(link_tag['href'])
            print(player_link)

# get data from Den team
den = tables[13].find('tbody').find_all('tr')[1:]

for player in den:    
    info = player.find_all('td')
    # print(info[:5])

    for cell in info:
        link_tag = cell.find('a')
        if link_tag and link_tag.get('href'):
            player_link = base_url + urllib.parse.unquote(link_tag['href'])
            print(player_link)
