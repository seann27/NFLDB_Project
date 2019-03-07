import mysql.connector
import logging
import datetime
import re
import sys
import bs4
import gc
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from team_dictionary import Team_Dictionary

# initialize logger
timeid = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
baseurl = 'C:\\Users\\skbla\\NFLDB_logs\\'
logfile = (baseurl+'scrape_gameinfo_'+timeid+'.log')
logging.basicConfig(level=logging.DEBUG,filename=logfile,filemode='w',format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')

# initialize db connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)
mycursor = mydb.cursor()

# returns page soup object
def get_soup(link):
    uClient = uReq(link)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "lxml")
    return page_soup

# utility method for parsing game page tables
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

# player class and methods
class Player:
    def __init__(self,gameid,playerid):
        self.game_id = gameid
        self.player_id = playerid
        self.player_teamid = 'null'
        self.opponent = 'null'
        self.pass_att = 0
        self.pass_comp = 0
        self.pass_yards = 0
        self.pass_tds = 0
        self.pass_int = 0
        self.rush_att = 0
        self.rush_yards = 0
        self.rush_tds = 0
        self.rec_tgts = 0
        self.rec = 0
        self.rec_yards = 0
        self.rec_tds = 0
        self.rtn_tds = 0
        self.extra_pt = 0
        self.fmb_lost = 0
        self.snapcount = 0
        self.pct_snaps = 0
        self.dk_points = 0

    def get_points(self):
        points = 0
        points += self.pass_yards/25
        points += self.pass_tds*4
        if self.pass_yards >= 300:
            points += 3
        points -= self.pass_int
        points += self.rush_tds*6
        points += self.rush_yards/10
        if self.rush_yards >= 100:
            points += 3
        points += self.rec
        points += self.rec_tds*6
        points += self.rec_yards/10
        if self.rec_yards >= 100:
            points += 3
        points += self.rtn_tds*6
        points += self.extra_pt
        points -= self.fmb_lost
        return points

# scrapes game info and inserts into database
def scrape_game_info(page_soup):
    # get game info
    # gameteams = page_soup.find("div",{"id":"content","role":"main"}).find("h1")
    # gameteams = re.split("\sat\s|-",gameteams.text)
    gameteams = page_soup.findAll("a",{"itemprop":"name"})
    team_home = gameteams[0]['href']
    team_away = gameteams[1]['href']
    team_home_name = gameteams[0].text
    team_away_name = gameteams[1].text
    gameteams = {team_home_name:team_home,team_away_name:team_away,team_home:team_away,team_away:team_home}
    gameinfo = page_soup.find("div",{"id":"all_game_info"})
    comment = gameinfo.find(string=lambda text:isinstance(text,Comment))
    gameinfo = soup(comment,"lxml")
    gameinfo = [tr.findAll("td") for tr in gameinfo.findAll("tr",{"class":None})]
    vegasline = gameinfo[-2][0].text.strip()
    vegasline = re.split("\s-",vegasline)
    if vegasline[0] == team_away:
        vegasline = vegasline[1]*-1
    else:
        vegasline = vegasline[1]
    overunder = float(gameinfo[-1][0].text.split(" ")[0].strip())
    score = page_soup.findAll("div",{"class":"score"})
    points_home = float(score[0].text.strip())
    points_away = float(score[1].text.strip())
    debugstr = (str(season)+" | "+str(week)+" | "+gameid+" | "+team_home+" | "+str(points_home)+" | "+team_away+" | "+str(points_away)+" | "+str(vegasline)+" | "+str(overunder))
    sql = "INSERT INTO nfl_games ("
    sql += "id,season,week,team_home,points_home,team_away,points_away,spread_visitor,over_under) "
    sql += "values (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    sql += "ON DUPLICATE KEY UPDATE team_home=(%s),points_home=(%s),team_away=(%s),points_away=(%s),spread_visitor=(%s),over_under=(%s)"
    sql_val = (
    	gameid,season,week,team_home,points_home,team_away,points_away,vegasline,overunder,
    	team_home,points_home,team_away,points_away,vegasline,overunder
    )
    # try:
    # 	mycursor.execute(sql,sql_val)
    # except mysql.connector.Error as msg:
    # 	error = debugstr+"\n"+sql+"\n"+str(msg)
    # 	logging.error(error)
    return gameteams

# scrapes all offensive stats for game and insert into database
misc_players = []
def scrape_offensive_stats(gameteams):
	player_list = {}
	# players,stats = get_data("all_player_offense",1)
	# for player,stat in zip(players,stats):
	# 	playerid = player.a['href']
	# 	p_obj = Player(gameid,playerid)
	# 	p_obj.player_teamid = gameteams[Team_Dictionary().football_ref[stat[0].text]]
	# 	p_obj.opponent = gameteams[p_obj.player_teamid]
	# 	p_obj.pass_comp = float(stat[1].text)
	# 	p_obj.pass_att = float(stat[2].text)
	# 	p_obj.pass_yards = float(stat[3].text)
	# 	p_obj.pass_tds = float(stat[4].text)
	# 	p_obj.pass_int = float(stat[5].text)
	# 	p_obj.rush_att = float(stat[10].text)
	# 	p_obj.rush_yards = float(stat[11].text)
	# 	p_obj.rush_tds = float(stat[12].text)
	# 	p_obj.rec_tgts = float(stat[14].text)
	# 	p_obj.rec = float(stat[15].text)
	# 	p_obj.rec_yards = float(stat[16].text)
	# 	p_obj.rec_tds = float(stat[17].text)
	# 	p_obj.fmb_lost = float(stat[20].text)
	# 	p_obj.rtn_tds = 0
	# 	p_obj.extra_pt = 0
	# 	player_list[playerid] = p_obj
    #
	# # get misc stats (special teams tds, 2pt conversions)
	# players,stats = get_data("all_scoring")
	# for stat in stats:
	# 	if re.search(r'return',stat[2].text) and re.search(r'interception',stat[2].text) is None and re.search(r'fumble',stat[2].text) is None:
	# 		print(stat[2].a['href'])
	# 		playerid = stat[2].a['href']
	# 		if playerid in player_list:
	# 			player_list[playerid].rtn_tds += 1
	# 		else:
	# 			misc_player = Player(gameid,playerid)
	# 			misc_player.link = link
	# 			misc_player.reason = "no offensive stats"
	# 			misc_players.append(misc_player)
	# 	if re.search(r'kick',stat[2].text) or re.search(r'failed',stat[2].text):
	# 		continue
	# 	else:
	# 		switch = 0
	# 		xp = 0
	# 		for item in stat[2]:
	# 			if item == ' (':
	# 				switch = 1
	# 			if switch == 1 and re.search(r'href',str(item)):
	# 				xp += 1
	# 		xp *= -1
	# 		players = stat[2].findAll('a')
	# 		while xp < 0:
	# 			playerid = players[xp].a['href']
	# 			player_list[playerid].extra_pt += 2
	# 			xp += 1

	# get position, snapcounts to player objects
	players,stats = get_data("all_home_snap_counts",1)
	vis_players,vis_stats = get_data("all_vis_snap_counts",1)
	players.extend(vis_players)
	stats.extend(vis_stats)
	for player,stat in zip(players,stats):
		playerid = player.a['href']
        player_list[playerid] = Player(gameid,playerid)
		# if playerid == '':
		# 	misc_player = Player(gameid,"unknown")
		# 	misc_player.link = link
		# 	misc_player.reason = "no name"
		# 	misc_players.append(misc_player)
		# 	logging.error("Could not get data for player on "+link)
		# 	continue
		# if playerid in player_list:
		player_list[playerid].position = stat[0].text
		player_list[playerid].snapcount_off = stat[1].text
		player_list[playerid].pct_snaps_off = float(stat[2].text.strip('%'))
        player_list[playerid].snapcount_def = stat[3].text
        player_list[playerid].pct_snaps_def = float(stat[4].text.strip('%'))
		# player_list[playerid].dk_points = player_list[playerid].get_points()
	for key,val in player_list.items():
		if hasattr(val,'snapcount'):
			# logging.debug("key: "+key+"\tplayerid: "+val.player_id)
			# build SQL insert statement
			sql = "INSERT INTO nfl_offense ("
			sql += "game_id,player_id,player_teamid,opponent,"
			sql += "pass_att,pass_comp,pass_yards,pass_tds,pass_int,"
			sql += "rush_att,rush_yards,rush_tds,"
			sql += "rec_tgts,rec,rec_yards,rec_tds,"
			sql += "rtn_tds,extra_points,fum_lost,snapcount,pct_snaps,dk_points) "
			sql += "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
			sql_val = (val.game_id,val.player_id,val.player_teamid,val.opponent,
	            val.pass_att,val.pass_comp,val.pass_yards,val.pass_tds,val.pass_int,
				val.rush_att,val.rush_yards,val.rush_tds,
	            val.rec_tgts,val.rec,val.rec_yards,val.rec_tds,
	            val.rtn_tds,val.extra_pt,val.fmb_lost,val.snapcount,val.pct_snaps,val.dk_points,
			)
			# try:
			# 	mycursor.execute(sql,sql_val)
			# except mysql.connector.Error as msg:
			# 	print("Command skipped: ",sql,sql_val, msg)
			# 	logging.error(msg)
			# if val.snapcount > 25:
			# 	print(val.id+", "+val.position+": "+str(val.dk_points))
		# else:
		# 	misc_player = Player(gameid,playerid)
		# 	misc_player.link = link
		# 	misc_player.reason = "no snapcount"
		# 	misc_players.append(misc_player)

# seasons = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
# weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
seasons = [2013]
weeks = [8]

for season in seasons:
	for week in weeks:
		link = "https://www.pro-football-reference.com/years/"+str(season)+"/week_"+str(week)+".htm"
		page_soup = get_soup(link)
		games = page_soup.findAll("td",{"class":"gamelink"})
		for game in games:
			gameid = str(game.a['href'])
			link = "https://www.pro-football-reference.com"+gameid
			page_soup = get_soup(link)
			gameteams = scrape_game_info(page_soup)
			scrape_offensive_stats(gameteams)
			mydb.commit()
			page_soup.decompose()

		print("----- finished games for week "+str(week))
	print("##### finished all weeks for season "+str(season))
    # gc.collect()
print("&&&&&&&&&&&&&&&&&&&& finished all seasons &&&&&&&&&&&&&&&&&&&&")
