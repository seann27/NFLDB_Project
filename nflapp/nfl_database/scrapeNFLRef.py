#!/usr/bin/python

import re
import mysql.connector
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq

team_links = []
team_names = []

link = "https://www.pro-football-reference.com/teams/"
uClient = uReq(link)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,"html.parser")
game_links = [th.find('a') for th in page_soup.findAll("th",{"scope":"row"},{"data-stat":"team_name"})]
for game in game_links:
	if game:
		team_link = ("https://www.pro-football-reference.com"+game['href']+"2018.htm")
		team_links.append(team_link)
		team_names.append(game.text)
# for link in team_links:
# 	print(link)

class player:
	def __init__(self,team,link,name):
		self.team = team
		self.link = link
		self.name = name

first = team_links[0]
# print(first)
# print(team_names[0])
uClient = uReq(first)
page_html = uClient.read()
uClient.close()

team_players = []
page_soup = soup(page_html,"html.parser")
passing = page_soup.find("div",{"id":"all_passing"})
rushing_receiving = page_soup.find("div",{"id":"all_rushing_and_receiving"})
kicking = page_soup.find("div",{"id":"all_kicking"})
qb = passing.find(text=lambda text:isinstance(text, Comment))
rb = rushing_receiving.find(text=lambda text:isinstance(text, Comment))
k = kicking.find(text=lambda text:isinstance(text, Comment))
qb_data = str(soup(qb,"html.parser"))
rb_data = str(soup(rb,"html.parser"))
k_data = str(soup(k,"html.parser"))
# <td class=left data-append-csv=RoseJo01 data-stat=player csk=Rosen,Josh ><a href=/players/R/RoseJo01.htm>Josh Rosen</a></td>
pattern = re.compile(r'data-stat=\"player\"(.+)(href=)(.+)>(.+)</a>')
qb_matches = pattern.findall(qb_data)
rb_matches = pattern.findall(rb_data)
k_matches = pattern.findall(k_data)
# print(qb_matches[0][2].strip('\"'))
# print(qb_matches[0][3])

team_players.append(player(team_names[0],qb_matches[0][2].strip('\"'),qb_matches[0][3]))

print(team_players[0].team)
print(team_players[0].link)
print(team_players[0].name)


# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="",
#   database="nfl_db"
# )
#
# mycursor = mydb.cursor()
# mycursor.execute("select * from nfl_database_teams")
# results = mycursor.fetchall()
# for result in results:
# 	print(result)
