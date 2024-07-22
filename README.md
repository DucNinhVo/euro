# Wikipedia Web Scraping - UEFA Euro 2024

## Introduction
This idea came to me when I was watching the match between Germany and Denmark in the knockout round of the Euro 2024 championship. During a corner kick situation, I noticed that the players of the Danish team were clearly taller than the players of the German team. I researched and found out that: according to wikipedia, the average height of Danish men ranks 4th in the world (181.9 cm) and the average height of German men ranks 16th (180.3 cm). However, if based only on this data, the difference is small. So to test my assertion, I had the idea to apply web scraping to collect data of the players and calculate the average height of the two teams.

## Process
This repository has 2 files: scrapping.py and euro.ipynb
- Run the scraping.py file first to scrape the necessary data from wikipedia. When running this file, the program will ask you to enter the name of the team you want to get information about, in this case I will enter Germany and Denmark. Note that you can only enter one team name each time you run the program
- These data will be saved to a csv file. There will be columns as follows
    - number: number of player
    - position: Defender (DF), Midfielder (MF) and Foward (FW) 
    - name
    - link: wikipedia link of the player  
    - caps: he number of official games a player has played for their national team
    - goals: number of goals scored by the player for the national team in official matches
    - nat_team: the national team the player is playing for
    - date_of_birth	
    - age	
    - place_of_birth	
    - height	
    - club: the current club the player is playing for 
- File euro.ipynb will be used to extract data from the csv file and perform calculations to verify the above assertion.
