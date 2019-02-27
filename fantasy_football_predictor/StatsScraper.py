import re
import mysql.connector
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from team_dictionary import Team_Dictionary

# establish global connection to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)
mycursor = mydb.cursor()

# define global web scraping initialization function
def get_soup(link):
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html,"html.parser")
	return page_soup

# main driver function
def scrape_all_stats(season,week):
	dks = ScrapeCurrentDKS(season,week)
	fpros = ScrapeFantasyPros(season,week)
	espn_proj = ScrapeEspnProjections(season,week)

	# driver
	dks.scrape()
	fpros.scrape()
	espn_proj.scrape()

class DkPlayer:
	def __init__(self,season,week,name,position,team,opp,salary):
		if position != 'D':
			name = name.split()
			name = str(name[0]+" "+name[1])
		self.name = name
		self.team = team
		self.opp = opp
		self.rid = str(season)+"-"+str(week)+"-"+name+"-"+position+"-"+team
		self.position = position
		self.salary = salary

# needs season/week as parameters, but scrapes most current week
class ScrapeCurrentDKS:
	def __init__(self,season,week):
		self.season = season
		self.week = week
		self.rotoguru_team_dict = Team_Dictionary().rotoguru_abbrev
		self.rotoguru_dst_dict = Team_Dictionary().rotoguru_dsts
		self.base_url_1 = "http://rotoguru1.com/cgi-bin/fstats.cgi?pos="
		self.base_url_2 = "&sort=3&game=p&colA=0&daypt=0&xavg=0&inact=0&maxprc=99999&outcsv=1"
		self.qb_url = "1"
		self.rb_url = "2"
		self.wr_url = "3"
		self.te_url = "4"
		self.dst_url = "7"

	# get large table of players
	def get_salary_string(self,pos_url):
		link = self.base_url_1+pos_url+self.base_url_2
		page_soup = get_soup(link)

		stats = page_soup.findAll("p")
		my_string = ""
		for stat in stats[1]:
			my_string = str(stat)
			break
		return my_string

	def get_players(self,pos):
		# split large table of players into lines
		player_list = []
		players = ''.join(self.get_salary_string(pos))
		players = players.splitlines()
		for player in players:
			if(re.search('^\d{4}',player)):
				stats = player.split(';')
				position = stats[1]
				team = stats[3].upper()
				team = self.rotoguru_team_dict[team]
				opp = stats[4].upper()
				opp = self.rotoguru_team_dict[opp]

				# process player name and defensive name from scraped values
				name = ""
				if pos != "7":
					fullname = stats[2].split(',')
					name = (fullname[1]+" "+fullname[0]).strip()
					name = name.split()
					name = name[0]+" "+name[1]
				else:
					abbrev = stats[2]
					name = self.rotoguru_dst_dict[abbrev]
				salary = stats[6]
				player_list.append(DkPlayer(self.season,self.week,name,position,team,opp,salary))
		return player_list

	def upload_players(self,pos):
		# insert player data into database
		pos_list = self.get_players(pos)
		for item in pos_list:
			sql = "INSERT INTO player_model (id,season,week,name,position,team,opp,dk_salary,played) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
			sql += "on duplicate key update dk_salary=(%s)"
			val = (item.rid,self.season,self.week,item.name,item.position,item.team,item.opp,item.salary,'n',item.salary)
			mycursor = mydb.cursor()
			mycursor.execute(sql,val)
			mydb.commit()

	# driver
	def scrape(self):
		self.upload_players(self.qb_url)
		print("DKS QBs updated")
		self.upload_players(self.rb_url)
		print("DKS RBs updated")
		self.upload_players(self.wr_url)
		print("DKS WRs updated")
		self.upload_players(self.te_url)
		print("DKS TEs updated")
		self.upload_players(self.dst_url)
		print("DKS DSTs updated")

class FpPlayer:
	def __init__(self,name,position,rank):
		self.name = name
		if position=='DST':
			position='D'
		self.position = position
		self.rank = rank

# needs season/week as parameters, but scrapes most current week
class ScrapeFantasyPros:
	def __init__(self,season,week):
		self.season = season
		self.week = week
		self.base_url = "https://www.fantasypros.com/nfl/rankings/"
		self.qb_url = self.base_url+"qb.php"
		self.rb_url = self.base_url+"rb.php"
		self.wr_url = self.base_url+"wr.php"
		self.te_url = self.base_url+"te.php"
		self.dst_url = self.base_url+"dst.php"
		self.fantasy_pros_dict = Team_Dictionary().fantasy_pros

	def scrape_fp(self,link):
		page_soup = get_soup(link)

		player_list = []
		players = page_soup.findAll("tr",{"class":"player-row"})
		for item in players:
			position = item.input['data-position']
			player_name =  item.find("span",{"class":"full-name"}).text
			stats = item.findAll("td",{"class":"ranks"})
			rank = stats[2].text
			rank = float(rank)
			player_list.append(FpPlayer(player_name,position,rank))

		return player_list

	def upload_players(self,player_list,pos):
		for item in player_list:
			sql = "select name,team from player_model where name like %s and name like %s and position = %s and week = %s"
			name = item.name
			val = ""
			if item.position == 'D':
				name = name.split("(")[1].strip("(").strip(")")
				name = self.fantasy_pros_dict[name]
				val = ('%'+name+'%','%'+name+'%',item.position,self.week,)
			else:
				name = name.split()
				first_name = name[0]
				last_name = name[1]
				val = ('%'+first_name+'%','%'+last_name+'%',item.position,self.week,)
			mycursor = mydb.cursor()
			mycursor.execute(sql,val)
			results = mycursor.fetchone()
			if results:
				name = results[0]
				team = results[1]
				rid = str(self.season)+"-"+str(self.week)+"-"+name+"-"+item.position+"-"+team
				sql = "INSERT INTO player_model (id,season,week,name,position,team,fp_rank,played) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
				sql += "ON DUPLICATE KEY UPDATE fp_rank=(%s)"
				val = (rid,self.season,self.week,name,item.position,team,item.rank,'n',item.rank)
				mycursor.execute(sql,val)
			else:
				continue

		mydb.commit()

	def validate_rankings(self):
		sql = "select p.id,e.proj_points "
		sql += "from player_model p, espn_player_projections e "
		sql += "where p.id=e.id "
		sql += "and p.week=%s "
		sql += "and p.fp_rank is null"
		val = (self.week,)
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
	def scrape(self):
		self.upload_players(self.scrape_fp(self.qb_url),'QB')
		print("Fantasy Pro QBs updated")
		self.upload_players(self.scrape_fp(self.rb_url),'RB')
		print("Fantasy Pro RBs updated")
		self.upload_players(self.scrape_fp(self.wr_url),'WR')
		print("Fantasy Pro WRs updated")
		self.upload_players(self.scrape_fp(self.te_url),'TE')
		print("Fantasy Pro TEs updated")
		self.upload_players(self.scrape_fp(self.dst_url),'D')
		print("Fantasy Pro Ds updated")
		self.validate_rankings()

# needs season/week as parameters, scrapes that week's url
class ScrapeEspnProjections:
	def __init__(self,season,week):
		self.season = season
		self.week = week
		self.espn_dict = Team_Dictionary().espn_proj

	def create_links(self):
		week = str(self.week)
		season = str(self.season)
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

	def upload_db(self,link):
		page_soup = get_soup(link)
		season = self.season
		week = self.week
		players = page_soup.findAll("tr",{"class":"pncPlayerRow"})
		for player in players:
			name = player.a.contents[0].strip()
			name = name.split()
			name = str(name[0]+" "+name[1])
			position = player.contents[0].contents[1].strip().split()[2].strip(',')
			team = player.contents[0].contents[1].strip().split()[1].upper()
			if team != 'FA':
				team = self.espn_dict[team]
			opp = player.contents[1].text.strip('@').upper()
			if opp != '** BYE **':
				opp = self.espn_dict[opp]
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
			else:
				pid = str(season)+"-"+str(week)+"-"+name+"-"+position+"-"+team
				stats = player.findAll("td")
				pass_yds = float(stats[3].text)
				pass_td = float(stats[4].text)
				pass_int = float(stats[5].text)
				rush_att = float(stats[6].text)
				rush_yds = float(stats[7].text)
				rush_td = float(stats[8].text)
				rec = float(stats[9].text)
				rec_yds = float(stats[10].text)
				rec_td = float(stats[11].text)
				# calculate projected points
				proj_points = pass_yds/25
				proj_points += pass_td/4
				proj_points -= (pass_int*2)
				proj_points += rush_yds/10
				proj_points += rush_td*6
				proj_points += rec
				proj_points += rec_yds/10
				proj_points += rec_td*6
			proj_dk = 0

			sql = "INSERT INTO espn_player_projections (id,season,week,name,position,team,opp,pass_yds,pass_td,pass_int,rush_att,rush_yds,rush_td,rec,rec_yds,rec_td,proj_points,proj_dk) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			sql += " ON DUPLICATE KEY UPDATE pass_yds=(%s),pass_td=(%s),pass_int=(%s),rush_att=(%s),rush_yds=(%s),rush_td=(%s),rec=(%s),rec_yds=(%s),rec_td=(%s),proj_points=(%s),proj_dk=(%s)"
			val = (pid,season,week,name,position,team,opp,pass_yds,pass_td,pass_int,rush_att,rush_yds,rush_td,rec,rec_yds,rec_td,proj_points,proj_dk,pass_yds,pass_td,pass_int,rush_att,rush_yds,rush_td,rec,rec_yds,rec_td,proj_points,proj_dk)
			mycursor = mydb.cursor()
			mycursor.execute(sql,val)
		mydb.commit()

	def upload_def_db(self,link):
		week = self.week
		season = self.season
		page_soup = get_soup(link)
		players = page_soup.findAll("tr",{"class":"pncPlayerRow"})

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
			stats = player.findAll("td")
			if stats[1].text != '** BYE **':
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

	def scrape(self):
		season = self.season
		week = self.week
		links,def_link = self.create_links()
		for link in links:
			self.upload_db(link)
		print(str(week)+" - Player projections uploaded")
		self.upload_def_db(def_link)
		print(str(week)+" - DST projections uploaded")

if __name__ == "__main__":
	scrape_all_stats(2018,16)
