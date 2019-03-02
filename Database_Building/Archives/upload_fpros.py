import re
import sys
import mysql.connector
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from team_dictionary import Team_Dictionary

# global variables
base_url = "https://www.fantasypros.com/nfl/rankings/"
qb = base_url+"qb.php"
rb = base_url+"rb.php"
wr = base_url+"wr.php"
te = base_url+"te.php"
dst = base_url+"dst.php"

season = 2018
week = 15
fantasy_pros_dict = Team_Dictionary().fantasy_pros
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)

class Player:
	def __init__(self,name,position,rank):
		self.name = name
		if position=='DST':
			position='D'
		self.position = position
		self.rank = rank

def scrape_fp(link):
	player_list = []
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html,"html.parser")

	players = page_soup.findAll("tr",{"class":"player-row"})
	for item in players:
		position = item.input['data-position']
		player_name =  item.find("span",{"class":"full-name"}).text
		stats = item.findAll("td",{"class":"ranks"})
		rank = stats[2].text
		rank = float(rank)
		player_list.append(Player(player_name,position,rank))

	return player_list

def upload_players(player_list,pos):
	for item in player_list:
		sql = "select name,team from player_model where name like %s and name like %s and position = %s and week = %s"
		name = item.name
		val = ""
		if item.position == 'D':
			name = name.split("(")[1].strip("(").strip(")")
			name = fantasy_pros_dict[name]
			val = ('%'+name+'%','%'+name+'%',item.position,week,)
		else:
			name = name.split()
			first_name = name[0]
			last_name = name[1]
			val = ('%'+first_name+'%','%'+last_name+'%',item.position,week,)
		mycursor = mydb.cursor()
		# print(val)
		mycursor.execute(sql,val)
		results = mycursor.fetchone()
		if results:
			name = results[0]
			team = results[1]
			rid = str(season)+"-"+str(week)+"-"+name+"-"+item.position+"-"+team
			# print(rid+"\t"+str(item.rank))
			sql = "INSERT INTO player_model (id,season,week,name,position,team,fp_rank,played) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
			sql += "ON DUPLICATE KEY UPDATE fp_rank=(%s)"
			val = (rid,season,week,name,item.position,team,item.rank,'n',item.rank)
			mycursor.execute(sql,val)
		else:
			continue
	mydb.commit()

def validate_rankings():
	sql = "select p.id,e.proj_points "
	sql += "from player_model p, espn_player_projections e "
	sql += "where p.id=e.id "
	sql += "and p.week=%s "
	sql += "and p.fp_rank is null"
	val = (week,)
	mycursor = mydb.cursor()
	mycursor.execute(sql,val)
	results = mycursor.fetchall()
	errors = 0
	for result in results:
		if result[1] > 5:
			print("Error! "+result[0]+" is projected points but has no ranking")
			errors +=1
		if errors > 0:
			print("Validation failed - "+str(errors)+" errors detected.")
		else:
			print("Success, players validated")

# driver
qbs = scrape_fp(qb)
rbs = scrape_fp(rb)
wrs = scrape_fp(wr)
te = scrape_fp(te)
dst = scrape_fp(dst)
upload_players(qbs,'QB')
print("QBs updated")
upload_players(rbs,'RB')
print("RBs updated")
upload_players(wrs,'WR')
print("WRs updated")
upload_players(te,'TE')
print("TEs updated")
upload_players(dst,'D')
print("Ds updated")
validate_rankings()
