# import here
import pandas as pd
import numpy as np
import os.path
from sqlalchemy import create_engine
from NFL_RefMaps import TeamDictionary
from NFL_Metrics import SkillPoints
from scrapers import PFR_Gamelinks,PFR_Gamepage

# connect to database
print("Setting up database connections . . .")
kaggle_engine = create_engine('mysql+pymysql://root:@localhost:3306/kaggle')
kaggle_conn = kaggle_engine.connect()
nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
main_engine = nfldb_engine.connect()
file = ("D:\\NFLDB\\game_info.csv")

# trim csv file to relevant stats for weeks 1-16, 2009-2018
print("Reading db csv file . . .")
gameinfo = pd.read_csv(file)

print("Dropping unused columns . . .")
# drop playoff weeks
indexNames = gameinfo[ gameinfo['schedule_playoff'] == True ].index
gameinfo.drop(indexNames,inplace=True)

# drop stats older than 2009
indexNames = gameinfo[ gameinfo['schedule_season'] < 2009 ].index
gameinfo.drop(indexNames,inplace=True)

# drop unused columns
gameinfo.drop(['schedule_playoff'],axis=1,inplace=True)
gameinfo.drop(['stadium'],axis=1,inplace=True)
gameinfo.drop(['stadium_neutral'],axis=1,inplace=True)
gameinfo.drop(['weather_temperature'],axis=1,inplace=True)
gameinfo.drop(['weather_wind_mph'],axis=1,inplace=True)
gameinfo.drop(['weather_humidity'],axis=1,inplace=True)
gameinfo.drop(['weather_detail'],axis=1,inplace=True)

def get_home_favorite(row):
	home_team = row['team_home']
	home_abbrev = TeamDictionary().nfl_api[home_team]
	if home_abbrev == row['team_favorite_id']:
		return 1
	elif row['team_favorite_id'] == 'PICK':
		return 0
	else:
		return -1

def get_spread_result(row):
	score_fav = 0
	score_und = 0
	spread = row['spread_favorite']*-1
	if(row['home_favorite']==1):
		score_fav = row['score_home']
		score_und = row['score_away']
	else:
		score_fav = row['score_away']
		score_und = row['score_home']
	diff = score_fav-score_und
	if( diff > spread ):
		return 1
	elif( diff < spread ):
		return -1
	else:
		return 0

def get_OU_result(row):
	OU = float(row['over_under_line'])
	total = row['score_home']+row['score_away']
	if( total > OU ):
		return 1
	elif( total < OU ):
		return -1
	else:
		return 0

def get_index(row):
	date = row['schedule_date']
	comps = date.split('/')
	date = comps[2]+'-'+comps[0]+'-'+comps[1]
	return date+TeamDictionary().nfl_api[row['team_home']]

# # generate metrics for dataset, set index
print("Generating odds metrics for gameinfo table . . .")
gameinfo['home_favorite'] = gameinfo.apply (lambda row: get_home_favorite(row), axis=1)
gameinfo['spread_result'] = gameinfo.apply(lambda row: get_spread_result(row),axis=1)
gameinfo['OU_result'] = gameinfo.apply(lambda row: get_OU_result(row),axis=1)
gameinfo['idx'] = gameinfo.apply(lambda row: get_index(row),axis=1)
gameinfo.set_index('idx',inplace=True)

def get_pbpindex(row):
	team_name = row['home_team']
	comps = row['game_date'].split('/')
	date = comps[2]+'-'+str(comps[0]).zfill(2)+'-'+str(comps[1]).zfill(2)
	idx = date+team_name
	return idx

def map_pfrlinks():
	cols = ['idx','pfr_link']
	df = pd.DataFrame(columns=cols)
	seasons = np.arange(2009,2019).tolist()
	weeks = np.arange(1,18).tolist()
	data = {'idx':[],'gamelinks':[],'season':[],'week':[]}

	cache = os.path.exists('pfrlinks.txt')
	cache_links = []
	cache_indexes = {}
	if cache:
		cache = open('pfrlinks.txt','r')
		games = cache.readlines()
		for game in games:
			comps = game.split(',')
			link = comps[1].rstrip()
			cache_links.append(link)
			cache_indexes[link]=comps[0].strip()
		cache.close()
	file = open('pfrlinks.txt','a')

	for season in seasons:
		for week in weeks:
			print("\tScraping ",str(season),"-",str(week)," . . .")
			pfrg = PFR_Gamelinks(season,week)
			gamelinks = pfrg.get_game_links()
			for game in gamelinks:
				if(game not in cache_links):
					print("\t\tGame: ",game)
					data['gamelinks'].append(game)
					pfr = PFR_Gamepage(game)
					gameinfo = pfr.get_gameinfo()
					date = gameinfo[1]
					mm = date[4:6]
					yyyy = date[0:4]
					dd = date[6:8]
					date = yyyy+"-"+mm+"-"+dd
					home_team = gameinfo[2]
					teams = TeamDictionary().nfl_api
					data['idx'].append(date+teams[home_team])
					file.write(date+teams[home_team]+','+game+'\n')
				else:
					data['gamelinks'].append(game)
					data['idx'].append(cache_indexes[game])
				data['season'].append(season)
				data['week'].append(week)

	df = pd.DataFrame.from_dict(data)
	df.set_index('idx',inplace=True)
	file.close()
	return df

print("Getting gameids from nfl_api . . .")
# sql statement for getting gameids
sql = "select distinct(pbp.game_id) as game_id, pbp.home_team as home_team, pbp.game_date as game_date \
	   from nfl_pbp pbp \
	   order by pbp.game_id"
gameinfo_gameids = pd.read_sql_query(sql, kaggle_conn, index_col=None)
gameinfo_gameids['idx'] = gameinfo_gameids.apply(lambda row: get_pbpindex(row),axis=1)

gameinfo_gameids.set_index('idx',inplace=True)
gameinfo['game_id']=gameinfo_gameids['game_id']

print("Grabbing the matching pro-football-reference.com game links for each game . . .")
pfrlinks = map_pfrlinks()
gameinfo['pfr_gamelinks'] = pfrlinks['gamelinks']
gameinfo['season'] = pfrlinks['season']
gameinfo['week'] = pfrlinks['week']
gameinfo.set_index('game_id',inplace=True)

# home stats
home_rush_sql = "select game_id, posteam as home_abbrev, sum(yards_gained) as home_rush_yds, sum(rush_attempt) as home_rush_att,sum(rush_touchdown) as home_rush_tds \
  from nfl_pbp \
  where posteam = home_team \
  and play_type = 'run' \
group by game_id"

home_short_pass_sql = "select game_id,sum(yards_gained) as home_shortpass_yds, \
   sum(pass_attempt) as home_shortpass_att, \
   sum(complete_pass) as home_shortpass_completions, \
   sum(pass_touchdown) as home_shortpass_tds \
  from nfl_pbp \
  where play_type='pass' \
  and pass_length = 'short' \
  and posteam=home_team \
  group by game_id,posteam"

home_deep_pass_sql = "select game_id,sum(yards_gained) as home_deeppass_yds, \
   sum(pass_attempt) as home_deeppass_att, \
   sum(complete_pass) as home_deeppass_completions, \
   sum(pass_touchdown) as home_deeppass_tds \
  from nfl_pbp \
  where play_type='pass' \
  and pass_length = 'deep' \
  and posteam=home_team \
  group by game_id,posteam"

home_sacked_sql = "select game_id, \
	sum(sack) as home_sacked, \
	from nfl_pbp \
	where play_type = 'pass' \
	and posteam = home_team \
	group by game_id"

home_short_pass_int_sql = "select game_id, \
	sum(interception) as home_short_interceptions \
	from nfl_pbp \
	where play_type = 'pass' \
	and pass_length = 'short' \
	and posteam = home_team \
	group by game_id"

home_deep_pass_int_sql = "select game_id, \
	sum(interception) as home_deep_interceptions \
	from nfl_pbp \
	where play_type = 'pass' \
	and pass_length = 'deep' \
	and posteam = home_team \
	group by game_id"

print("Getting home stats . . .")
home_rush_mets = pd.read_sql_query(home_rush_sql, kaggle_conn, index_col=None)
home_rush_mets.set_index('game_id',inplace=True)
home_short_pass_mets = pd.read_sql_query(home_short_pass_sql, kaggle_conn, index_col=None)
home_short_pass_mets.set_index('game_id',inplace=True)
home_deep_pass_mets = pd.read_sql_query(home_deep_pass_sql, kaggle_conn, index_col=None)
home_deep_pass_mets.set_index('game_id',inplace=True)
# home_pass_defense_mets = pd.read_sql_query(home_pass_defense_total_sql, kaggle_conn, index_col=None)
# home_pass_defense_mets.set_index('game_id',inplace=True)
home_sacked_mets = pd.read_sql_query(home_sacked_sql, kaggle_conn, index_col=None)
home_sacked_mets.set_index('game_id',inplace=True)
home_short_pass_int_mets = pd.read_sql_query(home_short_pass_int_sql, kaggle_conn, index_col=None)
home_short_pass_int_mets.set_index('game_id',inplace=True)
home_deep_pass_int_mets = pd.read_sql_query(home_deep_pass_int_sql, kaggle_conn, index_col=None)
home_deep_pass_int_mets.set_index('game_id',inplace=True)

home_offense = home_rush_mets.merge(home_short_pass_mets,on='game_id')
home_offense = home_offense.merge(home_deep_pass_mets,on='game_id')
home_offense = home_offense.merge(home_pass_defense_mets,on='game_id')
print("Home stats generated.")

print("Getting away stats . . .")
# away stats
away_rush_sql = "select game_id, \
	posteam as away_abbrev, \
	sum(yards_gained) as away_rush_yds, \
	sum(rush_attempt) as away_rush_att, \
	sum(rush_touchdown) as away_rush_tds \
  from nfl_pbp \
  where posteam = away_team \
  and play_type = 'run' \
group by game_id"

away_short_pass_sql = "select game_id,sum(yards_gained) as away_shortpass_yds, \
   sum(pass_attempt) as away_shortpass_att, \
   sum(complete_pass) as away_shortpass_completions, \
   sum(pass_touchdown) as away_shortpass_tds \
  from nfl_pbp \
  where play_type='pass' \
  and pass_length = 'short' \
  and posteam = away_team \
  group by game_id,posteam"

away_deep_pass_sql = "select game_id,sum(yards_gained) as away_deeppass_yds, \
   sum(pass_attempt) as away_deeppass_att, \
   sum(complete_pass) as away_deeppass_completions, \
   sum(pass_touchdown) as away_deeppass_tds \
  from nfl_pbp \
  where play_type='pass' \
  and pass_length = 'deep' \
  and posteam = away_team \
  group by game_id,posteam"

away_sacked_sql = "select game_id, \
   sum(sack) as away_sacked, \
  from nfl_pbp \
  where play_type = 'pass' \
  and posteam = away_team \
  group by game_id"

away_short_pass_int_sql = "select game_id, \
 	sum(interception) as away_short_interceptions \
 	from nfl_pbp \
 	where play_type = 'pass' \
 	and pass_length = 'short' \
 	and posteam = away_team \
 	group by game_id"

away_deep_pass_int_sql = "select game_id, \
 	sum(interception) as away_deep_interceptions \
 	from nfl_pbp \
 	where play_type = 'pass' \
 	and pass_length = 'deep' \
 	and posteam = away_team \
 	group by game_id"

away_rush_mets = pd.read_sql_query(away_rush_sql, kaggle_conn, index_col=None)
away_rush_mets.set_index('game_id',inplace=True)
away_short_pass_mets = pd.read_sql_query(away_short_pass_sql, kaggle_conn, index_col=None)
away_short_pass_mets.set_index('game_id',inplace=True)
away_deep_pass_mets = pd.read_sql_query(away_deep_pass_sql, kaggle_conn, index_col=None)
away_deep_pass_mets.set_index('game_id',inplace=True)
# away_pass_defense_mets = pd.read_sql_query(away_pass_defense_total_sql, kaggle_conn, index_col=None)
# away_pass_defense_mets.set_index('game_id',inplace=True)
away_sacked_mets = pd.read_sql_query(away_sacked_sql, kaggle_conn, index_col=None)
away_sacked_mets.set_index('game_id',inplace=True)
away_short_pass_int_mets = pd.read_sql_query(away_short_pass_int_sql, kaggle_conn, index_col=None)
away_short_pass_int_mets.set_index('game_id',inplace=True)
away_deep_pass_int_mets = pd.read_sql_query(away_deep_pass_int_sql, kaggle_conn, index_col=None)
away_deep_pass_int_mets.set_index('game_id',inplace=True)

away_offense = away_rush_mets.merge(away_short_pass_mets,on='game_id')
away_offense = away_offense.merge(away_deep_pass_mets,on='game_id')
away_offense = away_offense.merge(away_pass_defense_mets,on='game_id')
print("Away stats generated.")

all_offense = home_offense.merge(away_offense,on='game_id')
game_summary = gameinfo.merge(all_offense,on='game_id')
game_summary.to_sql('nfl_game_summary', con=main_engine, if_exists='replace',index='game_id')

print("Processing skillpoints per game . . .")
game_summary_formatted = game_summary.copy().reset_index()
sp = SkillPoints()
skillpoints_df = sp.build_skillpoints_dataframe(game_summary_formatted)
skillpoints_df.to_sql('nfl_skillpoints', con=main_engine, if_exists='replace')
