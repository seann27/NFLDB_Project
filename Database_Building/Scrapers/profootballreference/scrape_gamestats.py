import re
import sys
import gc
import logging
import traceback
import datetime
import numpy as np
import pandas as pd
import bs4
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from references_dict import Team_Dictionary,DataFrameColumns
from analyze_play import Play_Analysis

# initialize logger
timeid = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
baseurl = 'C:\\Users\\skbla\\NFLDB_logs\\'
logfile = (baseurl+'scrape_gameinfo_'+timeid+'.log')
logging.basicConfig(level=logging.DEBUG,filename=logfile,filemode='w',format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')

# returns page soup object
def get_soup(link):
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "lxml")
	return page_soup

# utility method for parsing game page tables
def get_data(page_soup,id,commented=0):
	data = page_soup.find("div",{"id":id})
	if commented > 0:
		comment = data.find(string=lambda text:isinstance(text,Comment))
		data = soup(comment,"lxml")
	players = [tr.find("th",{"scope":"row"}) for tr in data.findAll("tr",{"class":None})]
	stats = [tr.findAll("td") for tr in data.findAll("tr",{"class":None})]
	players.pop(0)
	stats.pop(0)
	return players,stats

def get_pbp_data(page_soup):
	data = page_soup.find("div",{"id":'all_pbp'})
	comment = data.find(string=lambda text:isinstance(text,Comment))
	data = soup(comment,"lxml")
	pbp_data = data.findAll("td",{"data-stat":"detail"})
	return pbp_data

def convert_to_df(table,metrics):
	columns = DataFrameColumns().football_ref[table]
	metrics = np.asarray(metrics)
	df = pd.DataFrame(metrics,columns=columns)
	return df

def evaluate_metric(metric,type):
	if not metric:
		if type == 'float':
			return 0
		if type == 'string':
			return 'N/A'
	else:
		return metric

# classes
class GameInfo():
	def __init__(self,gameid,home,away):
		self.game_id = gameid
		self.home_id = home
		self.away_id = away

	def get_opponent(self,team):
		if team == self.home_name:
			return self.away_name
		else:
			return self.home_name

class Player:
	def __init__(self,gameid,id,team):
		self.gameid = gameid
		self.id = id
		self.team = team

		# all offense table stats
		self.passatt = 0
		self.passcomp = 0
		self.passyds = 0
		self.passtds = 0
		self.int = 0
		self.sacked = 0
		self.sacked_yds = 0
		self.rushatt = 0
		self.rushyds = 0
		self.rushtds = 0
		self.recatt = 0
		self.rec = 0
		self.recyds = 0
		self.rectds = 0
		self.fmb = 0

		# detailed rushing stats
		self.rushing = {}
		self.rushing['left'] = {
			'end': {
				'att' : 0,
				'yds' : 0,
				'tds' : 0
			},
			'guard': {
				'att' : 0,
				'yds' : 0,
				'tds' : 0
			},
			'tackle': {
				'att' : 0,
				'yds' : 0,
				'tds' : 0
			}
		}
		self.rushing['upthe'] = {
			'middle': {
				'att' : 0,
				'yds' : 0,
				'tds' : 0
			}
		}
		self.rushing['right'] = {
			'end': {
				'att' : 0,
				'yds' : 0,
				'tds' : 0
			},
			'guard': {
				'att' : 0,
				'yds' : 0,
				'tds' : 0
			},
			'tackle': {
				'att' : 0,
				'yds' : 0,
				'tds' : 0
			}
		}

		# detailed receiving stats
		self.receiving = {}
		self.receiving['short'] = {
			'left': {
				'att' : 0,
				'catches' : 0,
				'yds' : 0,
				'tds' : 0
			},
			'middle': {
				'att' : 0,
				'catches' : 0,
				'yds' : 0,
				'tds' : 0
			},
			'right': {
				'att' : 0,
				'catches' : 0,
				'yds' : 0,
				'tds' : 0
			}
		}
		self.receiving['deep'] = {
			'left': {
				'att' : 0,
				'catches' : 0,
				'yds' : 0,
				'tds' : 0
			},
			'middle': {
				'att' : 0,
				'catches' : 0,
				'yds' : 0,
				'tds' : 0
			},
			'right': {
				'att' : 0,
				'catches' : 0,
				'yds' : 0,
				'tds' : 0
			}
		}

	def summarize_offense(self):
		self.all_off_metrics = (
			self.gameid,
			self.id,
			self.team,
			self.passatt,
			self.passcomp,
			self.passyds,
			self.passtds,
			self.int,
			self.sacked,
			self.sacked_yds,
			self.rushatt,
			self.rushyds,
			self.rushtds,
			self.recatt,
			self.rec,
			self.recyds,
			self.rectds,
			self.fmb
		)

	def summarize_rushing(self):
		locations = ('end','guard','tackle')
		metrics = ('att','yds','tds')
		self.detailed_rush_metrics = [
			self.gameid,
			self.id,
			self.team
		]
		for l in locations:
			for m in metrics:
				self.detailed_rush_metrics.append(self.rushing['left'][l][m])
		for m in metrics:
			self.detailed_rush_metrics.append(self.rushing['upthe']['middle'][m])
		for l in locations:
			for m in metrics:
				self.detailed_rush_metrics.append(self.rushing['right'][l][m])

	def summarize_receiving(self):
		depths = ('short','deep')
		directions = ('left','middle','right')
		metrics = ('att','catches','yds','tds')
		self.detailed_rec_metrics = [
			self.gameid,
			self.id,
			self.team
		]
		for d in depths:
			for r in directions:
				for m in metrics:
					self.detailed_rec_metrics.append(self.receiving[d][r][m])

# scraper submethods
def scrape_game_info(page_soup):
	gameteams = page_soup.findAll("a",{"itemprop":"name"})
	gameinfo = GameInfo(gameid,gameteams[0]['href'],gameteams[1]['href'])
	gameinfo.home_name = gameteams[0].text
	gameinfo.away_name = gameteams[1].text
	game_information = page_soup.find("div",{"id":"all_game_info"})
	comment = game_information.find(string=lambda text:isinstance(text,Comment))
	game_information = soup(comment,"lxml")
	game_information = [tr.findAll("td") for tr in game_information.findAll("tr",{"class":None})]
	vegasline = game_information[-2][0].text.strip()
	if vegasline == 'Pick':
		vegasline == 0
	else:
		vegasline = re.split("\s-",vegasline)
		if vegasline[0] == gameinfo.away_id:
			vegasline = vegasline[1]*-1
		else:
			vegasline = vegasline[1]
	overunder = float(game_information[-1][0].text.split(" ")[0].strip())
	score = page_soup.findAll("div",{"class":"score"})
	points_home = float(score[0].text.strip())
	points_away = float(score[1].text.strip())
	values = [[
		gameid,
		season,
		week,
		gameinfo.home_id,
		points_home,
		gameinfo.away_id,
		points_away,
		vegasline,
		overunder
	]]
	df = convert_to_df('GAMEINFO',values)
	return gameinfo,df

# get position, snapcounts to player objects
def scrape_snapcounts(home_team,away_team,page_soup):
	relevant_positions = ('QB','WR','RB','TE')
	metrics = []
	player_team_dict = {}
	def parse_players(metrics,team,players,stats):
		for player,stat in zip(players,stats):
			if not player.a:
				playerid = 'N/A'
			else:
				playerid = player.a['href']
			name = player.text
			position = stat[0].text
			team = team
			player_team_dict[playerid] = Player(gameid,playerid,team)
			player_team_dict[playerid].position = position
			snapcount_off = stat[1].text
			snapcount_def = stat[3].text
			player_team_dict[playerid].snapcount_off = snapcount_off
			player_team_dict[playerid].snapcount_def = snapcount_def
			pct_snaps_off = float(stat[2].text.strip('%'))
			if position in relevant_positions:
				metrics.append([gameid,playerid,name,position,team,snapcount_off,pct_snaps_off])
	home_players,home_stats = get_data(page_soup,"all_home_snap_counts",1)
	away_players,away_stats = get_data(page_soup,"all_vis_snap_counts",1)
	parse_players(metrics,home_team,home_players,home_stats)
	parse_players(metrics,away_team,away_players,away_stats)
	df = convert_to_df('SNAPCOUNTS',metrics)
	return df,player_team_dict

def scrape_auxiliary_player_dict(page_soup):
	player_team_dict = {}
	off_players,off_stats = get_data(page_soup,'all_player_offense',1)
	def_players,def_stats = get_data(page_soup,'all_player_defense',1)
	drush_players,drush_stats = get_data(page_soup,'all_rush_directions',1)
	drec_players,drec_stats = get_data(page_soup,'all_targets_directions',1)


def scrape_offensive_stats(section,table,page_soup):
	metrics = []
	players,stats = get_data(page_soup,section,1)
	for player,stat in zip(players,stats):
		metric_list = [gameid]
		metric_list.append(player.text)
		for metric in stat:
			value = metric.text
			if not value:
				value = 0
			metric_list.append(value)
		metrics.append(metric_list)
	df = convert_to_df(table,metrics)
	return df

def scrape_defensive_stats(home_name,away_name,player_team_dict,page_soup):
	# define stats dictionary
	team_stats = {
		home_name: [gameid,home_name,0,0,0,0,0,0],
		away_name: [gameid,away_name,0,0,0,0,0,0]
	}

	# scrape summary defense stats
	players,stats = get_data(page_soup,'all_player_defense',1)
	for stat in stats:
		team = Team_Dictionary().football_ref[stat[0].text]
		team_stats[team][3] += float(evaluate_metric(stat[1].text,'float'))
		team_stats[team][2] += float(evaluate_metric(stat[6].text,'float'))
		team_stats[team][4] += float(evaluate_metric(stat[12].text,'float'))
		team_stats[team][5] += float(evaluate_metric(stat[3].text,'float'))
		team_stats[team][5] += float(evaluate_metric(stat[14].text,'float'))

	# find all instances of where a blocked punt/fg has occurred
	all_playdetails = get_pbp_data(page_soup)
	for play in all_playdetails:
		blocked = re.search('blocked',play.text)
		testing = re.search('extra point good',play.text)
		if blocked:
			player_tags = play.findAll('a')
			if len(player_tags) > 0:
				player_tags.pop(0)
				playerid = player_tags[0]['href']
				team = player_team_dict[playerid].team
				if team == home_name:
					team = away_name
				else:
					team == home_name
				team_stats[team][7] += 1

	# calculate how many 2-point plays happened
	home_team_score = 0
	away_team_score = 0
	misc,stats = get_data(page_soup,'all_scoring')
	for stat in stats:
		home_score = int(stat[4].text)
		away_score = int(stat[3].text)
		if (home_score - home_team_score) == 2:
			team_stats[home_name][6] += 1
		if (away_score - away_team_score) == 2:
			team_stats[away_name][6] += 1
		home_team_score = home_score
		away_team_score = away_score

	# convert stats dictionary to dataframe
	defense_metrics = [team_stats[home_name],team_stats[away_name]]
	metrics = np.asarray(defense_metrics)
	df = convert_to_df('DST',metrics)
	return df

def run_pipeline(link,season):
	print(link)
	page_soup = get_soup(link)
	# try:
	gameinfo,gameinfo_df = scrape_game_info(page_soup)
	snapcounts_df,player_team_dict = scrape_snapcounts(gameinfo.home_name,gameinfo.away_name,page_soup)
	all_pbp_analysis = Play_Analysis(get_pbp_data(page_soup),player_team_dict,season)
	all_offense_df = all_pbp_analysis.get_all_offense()
	detailed_rushing_df = all_pbp_analysis.get_detailed_rushing()
	detailed_passing_df = all_pbp_analysis.get_detailed_receiving()
	summary_defense_df = scrape_defensive_stats(gameinfo.home_name,gameinfo.away_name,player_team_dict,page_soup)
	page_soup.decompose()
	# except Exception as e:
	# 	logging.error(traceback.format_exc())

if __name__ == "__main__":
	# seasons = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
	weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
	seasons = [2014]
	# weeks = [6]
	for season in seasons:
		print("SEASON "+str(season))
		for week in weeks:
			print("WEEK "+str(week))
			link = "https://www.pro-football-reference.com/years/"+str(season)+"/week_"+str(week)+".htm"
			page_soup = get_soup(link)
			games = page_soup.findAll("td",{"class":"gamelink"})
			for game in games:
				gameid = str(game.a['href'])
				link = "https://www.pro-football-reference.com"+gameid
				run_pipeline(link,season)
		gc.collect()
