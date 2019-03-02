import re
import mysql.connector
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from team_dictionary import Team_Dictionary

link1 = "http://rotoguru1.com/cgi-bin/fstats.cgi?pos="
link2 = "&sort=3&game=p&colA=0&daypt=0&xavg=0&inact=0&maxprc=99999&outcsv=1"
qb = "1"
rb = "2"
wr = "3"
te = "4"
k = "6"
dst = "7"
season = 2018
week = 15

rotoguru_team_dict = Team_Dictionary().rotoguru_abbrev
rotoguru_dst_dict = Team_Dictionary().rotoguru_dsts

class Player:
	def __init__(self,name,position,team,opp,salary):
		if position != 'D':
			name = name.split()
			name = str(name[0]+" "+name[1])
		self.name = name
		self.team = team
		self.opp = opp
		self.rid = str(season)+"-"+str(week)+"-"+name+"-"+position+"-"+team
		self.position = position
		self.salary = salary

# get large table of players
def get_salary_string(pos):
	link = link1+pos+link2
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html,"html.parser")

	stats = page_soup.findAll("p")
	# print(str(stats[1]))
	my_string = ""
	for stat in stats[1]:
		my_string = str(stat)
		print(my_string)
		break
	return my_string

def get_players(pos):
	# split large table of players into lines
	player_list = []
	players = ''.join(get_salary_string(pos))
	players = players.splitlines()
	for player in players:
		if(re.search('^\d{4}',player)):
			stats = player.split(';')
			position = stats[1]
			team = stats[3].upper()
			team = rotoguru_team_dict[team]
			opp = stats[4].upper()
			opp = rotoguru_team_dict[opp]
			# process player name and defensive name from scraped values
			name = ""
			if pos != "7":
				fullname = stats[2].split(',')
				name = (fullname[1]+" "+fullname[0]).strip()
				name = name.split()
				name = name[0]+" "+name[1]
				print(name)
			else:
				abbrev = stats[2]
				name = rotoguru_dst_dict[abbrev]
				print(name)
			salary = stats[6]
			player_list.append(Player(name,position,team,opp,salary))
	return player_list

def upload_players(pos):
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="",
	  database="nfl_db"
	)

	pos_list = get_players(pos)
	for item in pos_list:
		sql = "INSERT INTO player_model (id,season,week,name,position,team,opp,dk_salary,played) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
		sql += "on duplicate key update dk_salary=(%s)"
		val = (item.rid,season,week,item.name,item.position,item.team,item.opp,item.salary,'n',item.salary)
		mycursor = mydb.cursor()
		mycursor.execute(sql,val)
		mydb.commit()

upload_players(qb)
upload_players(rb)
upload_players(wr)
upload_players(te)
upload_players(k)
upload_players(dst)
