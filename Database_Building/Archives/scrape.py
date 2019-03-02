import re
import bs4
import mysql.connector
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from team_dictionary import Team_Dictionary

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)
mycursor = mydb.cursor()

def get_soup(link):
    uClient = uReq(link)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "lxml")
    return page_soup

class Player:
    def __init__(self,name):
        self.name = name

def get_points(player):
    points = 0
    points += player.pass_yards/25
    points += player.pass_tds*4
    if player.pass_yards >= 300:
        points += 3
    points -= player.pass_int
    points += player.rush_tds*6
    points += player.rush_yards/10
    if player.rush_yards >= 100:
        points += 3
    points += player.rec
    points += player.rec_tds*6
    points += player.rec_yards/10
    if player.rec_yards >= 100:
        points += 3
    points += player.rtn_tds*6
    points += player.extra_pt
    points -= player.fmb_lost
    return points

def get_data(id,commented=0):
    data = page_soup.find("div",{"id":id})
    # print(". . . getting data for table id: "+id)
    if commented > 0:
        # print(". . . processing as comment...")
        comment = data.find(string=lambda text:isinstance(text,Comment))
        data = soup(comment,"lxml")
    players = [tr.find("th",{"scope":"row"}) for tr in data.findAll("tr",{"class":None})]
    stats = [tr.findAll("td") for tr in data.findAll("tr",{"class":None})]
    players.pop(0)
    stats.pop(0)
    return players,stats

weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# weeks = [5]
season = 2018
misc_players = []
# FULLTEAMS = []
for week in weeks:
	link = "https://www.pro-football-reference.com/years/2018/week_"+str(week)+".htm"
	page_soup = get_soup(link)
	games = page_soup.findAll("td",{"class":"gamelink"})
	print("=========================================== WEEK "+str(week)+" PERFORMANCES ===========================================")
	for game in games:
		player_list = {}
		link = "https://www.pro-football-reference.com"+str(game.a['href'])
		print()
		print("Accessing game "+link)
		page_soup = get_soup(link)

		# get core offensive stats
		players,stats = get_data("all_player_offense",1)
		for player,stat in zip(players,stats):
			name = player.text
			name = name.split()
			name = name[0]+" "+name[1]
			p_obj = Player(name)
			p_obj.team = Team_Dictionary().football_ref[stat[0].text]
			# if stat[0].text not in FULLTEAMS:
			# 	FULLTEAMS.append(stat[0].text)
			p_obj.pass_comp = float(stat[1].text)
			p_obj.pass_att = float(stat[2].text)
			p_obj.pass_yards = float(stat[3].text)
			p_obj.pass_tds = float(stat[4].text)
			p_obj.pass_int = float(stat[5].text)
			p_obj.rush_att = float(stat[10].text)
			p_obj.rush_yards = float(stat[11].text)
			p_obj.rush_tds = float(stat[12].text)
			p_obj.rec = float(stat[15].text)
			p_obj.rec_yards = float(stat[16].text)
			p_obj.rec_tds = float(stat[17].text)
			p_obj.fmb_lost = float(stat[20].text)
			p_obj.rtn_tds = 0
			p_obj.extra_pt = 0

			p_obj.week = week
			p_obj.season = season
			player_list[name] = p_obj

	    # get misc stats (special teams tds, 2pt conversions)
		players,stats = get_data("all_scoring")
		for stat in stats:
			if re.search(r'return',stat[2].text) and re.search(r'interception',stat[2].text) is None and re.search(r'fumble',stat[2].text) is None:
				name = stat[2].contents[0].text
				if name in player_list:
					player_list[name].rtn_tds += 1
				else:
					misc_player = Player(name)
					misc_player.link = link
					misc_player.reason = "no offensive stats"
					misc_players.append(misc_player)
			if re.search(r'kick',stat[2].text) or re.search(r'failed',stat[2].text):
				continue
			else:
				switch = 0
				xp = 0
				for item in stat[2]:
					if item == ' (':
						switch = 1
					if switch == 1 and re.search(r'href',str(item)):
						xp += 1
				xp *= -1
				players = stat[2].findAll('a')
				while xp < 0:
					name = players[xp].text
					player_list[name].extra_pt += 2
					xp += 1

		# get position, snapcounts to player objects
		players,stats = get_data("all_home_snap_counts",1)
		vis_players,vis_stats = get_data("all_vis_snap_counts",1)
		players.extend(vis_players)
		stats.extend(vis_stats)
		for player,stat in zip(players,stats):
			name = player.text
			if name == '':
				misc_player = Player("unknown")
				misc_player.link = link
				misc_player.reason = "no name"
				misc_players.append(misc_player)
				continue
			name = name.split()
			name = name[0]+" "+name[1]
			if name in player_list:
				player_list[name].position = stat[0].text
				player_list[name].snapcount = float(stat[2].text.strip('%'))
				player_list[name].dk_points = get_points(player_list[name])
				player_list[name].id = (str(player_list[name].season)+"-"+str(player_list[name].week)+"-"+player_list[name].name+"-"+player_list[name].position+"-"+player_list[name].team)
		for key,val in player_list.items():
			if hasattr(val,'snapcount'):
				# build SQL insert statement
				sql = "INSERT INTO individual_weekly_stats ("
				sql += "id,season,week,name,position,team,opponent,snapcount_percent,"
				sql += "rush_att,rush_yards,rush_tds,"
				sql += "receptions,rec_yards,rec_tds,"
				sql += "pass_att,pass_comp,pass_tds,pass_yards,pass_int,"
				sql += "rtn_tds,extra_points,fum_lost,dk_points) "
				sql += "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
				sql += "ON DUPLICATE KEY UPDATE dk_points=(%s)"
				sql_val = (
					val.id,
					val.season,
					val.week,
					val.name,
					val.position,
					val.team,
					"null",
					val.snapcount,
					val.rush_att,
					val.rush_yards,
					val.rush_tds,
					val.rec,
					val.rec_yards,
					val.rec_tds,
					val.pass_att,
					val.pass_comp,
					val.pass_tds,
					val.pass_yards,
					val.pass_int,
					val.rtn_tds,
					val.extra_pt,
					val.fmb_lost,
					val.dk_points,
					val.dk_points
				)
				mycursor.execute(sql,sql_val)
				if val.snapcount > 25:
					print(val.id+", "+val.position+": "+str(val.dk_points))
			else:
				misc_player = Player(key)
				misc_player.link = link
				misc_player.reason = "no snapcount"
				misc_players.append(misc_player)
		mydb.commit()

print("----------------------------------------------------")
# f = open('football_ref_abbrev.txt','w')
# for fteam in FULLTEAMS:
# 	f.write(fteam+"\n")
