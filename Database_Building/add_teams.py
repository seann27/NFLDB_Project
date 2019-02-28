import re
import mysql.connector
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)

sql = "select espnid from nfl_database_players"
mycursor = mydb.cursor()
mycursor.execute(sql)
results = mycursor.fetchall()

player_url = "http://www.espn.com/nfl/player/_/id/"

def update_player_teams(id,link):
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html,"html.parser")

	info = page_soup.find("ul",{"class":"general-info"})
	position = info.find("li",{"class":"first"}).text
	# print(id)
	if info.find("a") is not None:
		team = info.find("a").text
		position = position.split()[1].strip()
		# print(position+"\t"+team)

		sql = "update nfl_database_players set position=%s where espnid=%s"
		val = (position,id)
		mycursor.execute(sql,val)

def update_playermodel_teams():
	update player_model m set m.team =

counter = 1
for result in results:
	id = result[0]
	url = player_url+id
	update_player_teams(id,url)
	print(str(counter)+"/1983")
	counter += 1

mydb.commit()
