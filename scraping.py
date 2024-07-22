from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import ssl
import sys
import re
import pandas as pd
import os

def player_data(url):
    player_html = urlopen(url, context=ctx).read()
    player_soup = BeautifulSoup(player_html, "html.parser")

    player_table = player_soup.find('table',class_='infobox infobox-table vcard').find('tbody').find_all('tr')
   
    player_info = []
    for row in player_table:
        if row.find('th'):
            row_header = row.find('th').get_text(strip=True).lower()

            if row_header == 'date of birth':
                # Dob has format like this (1986-03-27)27 March 1986(age\xa038)
                dob_string = row.find('td').get_text(strip= True)
                dob_pattern = re.compile(r'\((\d{4}-\d{2}-\d{2})\).*?age\xa0(\d{2})') 
                matches = re.search(dob_pattern,dob_string)
                if matches:
                    dob = matches.group(1)
                    age = int(matches.group(2))
                player_info += [dob,age]
              
            if row_header == 'place of birth':
                pob = re.sub(r'\[\d+\]','',row.find('td').get_text(strip= True)) 
                player_info.append(pob)

            if row_header == 'height':
                # Get the height in m and convert to cm
                height_pattern = re.compile(r'(\d+(\.\d+)?)\s*m')
                height_string = row.find('td').get_text(strip= True) 
                height = float(re.search(height_pattern,height_string).group(1)) * 100
                player_info.append(height)

            if row_header == 'current team':
                club = row.find('td').get_text(strip= True)
                player_info.append(club)

    return player_info    

def team_data(team):
    team = team.strip().lower().capitalize()
    team_url = base_url + f"/wiki/{team}_national_football_team"

    # Exit if team is empty
    if not team:
        print('Invalid input')
        sys.exit(1)

    # Retrieve the html, 
    try: 
        html = urlopen(team_url, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")        
        sys.exit(1)

    # Locate the table
    target = soup.find('h3',string='Current squad')
    target_table = target.find_next('table')

    # Retrieve data
    team_list = list()
    rows = target_table.find_all('tr',class_='nat-fs-player')
    for row in rows:
        cells = row.find_all('td')
       
        number = cells[0].text.strip()
        position = re.findall(r'[a-zA-Z]+', cells[1].text.strip())[0] 
        name = row.find('th').text.strip()   
        link = base_url + row.find('th').find('a').get('href')         
        caps = int(cells[3].text)
        goals = int(cells[4].text)
            
        player_info = [number,position,name,link,caps,goals,team] + player_data(link)
        team_list.append(player_info)

    return team_list

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = "https://en.wikipedia.org"
# Input the team to get info

team = input('Enter the team - ')
team_list = team_data(team)

# Create a dataframe
df = pd.DataFrame(team_list,columns=['number','position','name','link','caps','goals','nat_team','date_of_birth','age','place_of_birth','height','club'])


# Path to the CSV file
csv_file_path = 'players.csv'

# Check if the file exists to decide if header is needed
header_needed = not os.path.isfile(csv_file_path)

# Save dataframe in csv file
df.to_csv(csv_file_path,mode='a',header=header_needed,index=False)
print("Data saved to players.csv")
