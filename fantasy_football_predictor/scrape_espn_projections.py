import re
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import mysql.connector

def create_links(season,week):
	links = []
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=0&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=0")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=2&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=0")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=2&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=40")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=2&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=80")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=4&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=0")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=4&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=40")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=4&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=80")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=4&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=120")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=6&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=0")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=6&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=40")
	links.append("http://games.espn.com/ffl/tools/projections?&slotCategoryId=6&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=80")

	def_link = "http://games.espn.com/ffl/tools/projections?&slotCategoryId=16&scoringPeriodId="+week+"&seasonId="+season+"&startIndex=0"

	return links,def_link

def upload_db(link,season,week):
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html,"html.parser")

	players = page_soup.findAll("tr",{"class":"pncPlayerRow"})

	# class PlayerStats:
	# 	def __init__(self,pass_yds,pass_td,pass_int,rush_att,rush_yds,rush_td,rec,rec_yds,rec_td,points):
	# 		self.pass_yds = pass_yds
	# 		self.pass_td = pass_td
	# 		self.pass_int = pass_int
	# 		self.rush_att = rush_att
	# 		self.rush_yds = rush_yds
	# 		self.rush_td = rush_td
	# 		self.rec = rec
	# 		self.rec_yds = rec_yds
	# 		self.rec_td = rec_td
	# 		self.points = points

	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="",
	  database="nfl_db"
	)

	for player in players:
		# pid = player.a["playerid"]
		# print(pid)
		name = player.a.contents[0].strip()
		name = name.split()
		name = str(name[0]+" "+name[1])
		position = player.contents[0].contents[1].strip().split()[2]
		sql = "select t.city,t.name from nfl_database_teams t, nfl_database_players p where p.team_id=t.id and p.name like %s and p.position = %s"
		# val = (pid,)
		val = ('%'+name+'%',position,)
		mycursor = mydb.cursor()
		mycursor.execute(sql,val)
		results = mycursor.fetchone()
		if results:
			team = results[0]+" "+results[1]
		else:
			team = "unknown"
		# name = results[0]
		# position = results[1]
		# team = results[2]
		print(name+"\t"+position+"\t"+team)
		# exit()
		pid = str(season)+"-"+str(week)+"-"+name+"-"+position+"-"+team
		stats = player.findAll("td")
		if float(stats[13].text) < 1:
			break
		pass_yds = float(stats[4].text)
		pass_td = float(stats[5].text)
		pass_int = float(stats[6].text)
		rush_att = float(stats[7].text)
		rush_yds = float(stats[8].text)
		rush_td = float(stats[9].text)
		rec = float(stats[10].text)
		rec_yds = float(stats[11].text)
		rec_td = float(stats[12].text)
		proj_points = float(stats[13].text)

		sql = "INSERT INTO espn_player_projections (id,season,week,name,position,team,pass_yds,pass_td,pass_int,rush_att,rush_yds,rush_td,rec,rec_yds,rec_td,proj_points) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		sql += " ON DUPLICATE KEY UPDATE pass_yds=(%s),pass_td=(%s),pass_int=(%s),rush_att=(%s),rush_yds=(%s),rush_td=(%s),rec=(%s),rec_yds=(%s),rec_td=(%s),proj_points=(%s)"
		val = (pid,season,week,name,position,team,pass_yds,pass_td,pass_int,rush_att,rush_yds,rush_td,rec,rec_yds,rec_td,proj_points,pass_yds,pass_td,pass_int,rush_att,rush_yds,rush_td,rec,rec_yds,rec_td,proj_points)
		mycursor = mydb.cursor()
		mycursor.execute(sql,val)

	mydb.commit()

def upload_def_db(link,season,week):
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html,"html.parser")

	players = page_soup.findAll("tr",{"class":"pncPlayerRow"})

	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="",
	  database="nfl_db"
	)
	mycursor = mydb.cursor()
	for player in players:
		name = player.a.contents[0].strip()
		name = name.split()[0]
		sql = "select city,name from nfl_database_teams where name=%s"
		val=(name,)
		mycursor.execute(sql,val)
		result = mycursor.fetchone()
		name = result[0]+" "+result[1]
		pid = str(season)+"-"+str(week)+"-"+name+"-D-"+name
		print(pid)
		stats = player.findAll("td")
		sacks = stats[4].text
		forced_fum = stats[5].text
		recovered_fum = stats[6].text
		interceptions = stats[7].text
		pick_six = stats[8].text
		fum_td = stats[9].text
		proj_points = stats[10].text

		sql = "INSERT INTO espn_defense_projections (id,season,week,name,sacks,forced_fum,recovered_fum,interceptions,pick_six,fum_td,proj_points) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		sql += " ON DUPLICATE KEY UPDATE sacks=(%s),forced_fum=(%s),recovered_fum=(%s),interceptions=(%s),pick_six=(%s),fum_td=(%s),proj_points=(%s)"
		val = (pid,season,week,name,sacks,forced_fum,recovered_fum,interceptions,pick_six,fum_td,proj_points,sacks,forced_fum,recovered_fum,interceptions,pick_six,fum_td,proj_points)
		mycursor.execute(sql,val)
	mydb.commit()

# driver
season = 2018
week = 15
links,def_link = create_links(str(season),str(week))
for link in links:
	upload_db(link,season,week)
upload_def_db(def_link,str(season),str(week))
# add first 13 weeks ot projections to database
# for x in range(13):
# 	y = x+1
# 	links,def_link = create_links("2018",str(y))
# 	for link in links:
# 		upload_db(link,2018,y)
# 	upload_def_db(def_link,"2018",str(y))
