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
baseurl = 'C:\\Users\\skbla\\NFLDB_Project\\Database_Building\\'
logfile = (baseurl+'logs\\scrape_gameinfo_'+timeid+'.log')
logging.basicConfig(level=logging.DEBUG,filename=logfile,filemode='w',format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')

# # initialize db connection
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

seasons = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
# seasons = [2018]
# weeks = [5]

for season in seasons:
	for week in weeks:
		link = "https://www.pro-football-reference.com/years/"+str(season)+"/week_"+str(week)+".htm"
		page_soup = get_soup(link)
		games = page_soup.findAll("td",{"class":"gamelink"})
		for game in games:
			gameid = str(game.a['href'])
			link = "https://www.pro-football-reference.com"+gameid
			page_soup = get_soup(link)

            # get game info
			gameteams = page_soup.find("div",{"id":"content","role":"main"}).find("h1")
			gameteams = re.split("\sat\s|-",gameteams.text)
			team_away = gameteams[0].strip()
			team_home = gameteams[1].strip()
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
			try:
				mycursor.execute(sql,sql_val)
			except mysql.connector.Error as msg:
				error = debugstr+"\n"+sql+"\n"+str(msg)
				logging.error(error)
			mydb.commit()
            page_soup.decompose()

		print("----- finished games for week "+str(week))
	print("##### finished all weeks for season "+str(season))
    gc.collect()
print("&&&&&&&&&&&&&&&&&&&& finished all seasons &&&&&&&&&&&&&&&&&&&&")
