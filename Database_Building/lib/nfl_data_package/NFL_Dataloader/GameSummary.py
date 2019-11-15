import pandas as pd
import numpy as np
import os.path
from sqlalchemy import create_engine
from NFL_RefMaps import TeamDictionary
from NFL_Metrics import SkillPoints
from scrapers import PFR_Gamelinks,PFR_Gamepage

nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
main_engine = nfldb_engine.connect()

gameinfo_cols = [
    'gameid',
    'date',
    'team_home',
    'points_home',
    'team_away',
    'points_away',
    'home_fav',
    'vegasline',
    'overunder',
    'ats_result',
    'ou_result'
]

def get_pbpindex(row):
	team_name = row['home_team']
	comps = row['game_date'].split('/')
	date = comps[2]+'-'+str(comps[0]).zfill(2)+'-'+str(comps[1]).zfill(2)
	idx = date+team_name
	return idx

def map_pfrlinks(season,week,gamelinks):
    # initialize dictionary
	data = {'idx':[],'gamelinks':[],'season':[],'week':[]}

    # read in cached data if it exists
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

    # scrape games
	print("\tScraping ",str(season),"-",str(week)," . . .")
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

class GameSummary:

    def __init__(self,season,week):
        self.season = season
        self.week = week

    def get_summary(self):
        gamelinks = PFR_Gamelinks.get_game_links(self.season,self.week)

        # build gameinfo base dataframe
        for link in gamelinks:
            game = PFR_Gamepage(link)
            gameinfo = game.get_gameinfo()

        # extract gameids from API play by play table
        print("Getting gameids from nfl_api . . .")
        sql = "select distinct(pbp.game_id) as game_id, pbp.home_team as home_team, pbp.game_date as game_date \
        	   from nfl_pbp pbp \
               where season = :season \
               and week = :week \
        	   order by pbp.game_id"
        gameinfo_gameids = pd.read_sql_query(sql, main_engine, params=(season,week), index_col=None)
        gameinfo_gameids['idx'] = gameinfo_gameids.apply(lambda row: get_pbpindex(row),axis=1)
        gameinfo_gameids.set_index('idx',inplace=True)
        gameinfo['game_id']=gameinfo_gameids['game_id']

        # add pro-football-reference links
        pfrlinks = map_pfrlinks(self.season,self.week,gamelinks)
        gameinfo['pfr_gamelinks'] = pfrlinks['gamelinks']

        # add season/week
        gameinfo['season'] = pfrlinks['season']
        gameinfo['week'] = pfrlinks['week']
        gameinfo.set_index('game_id',inplace=True)

        # get home offensive stats
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

        # get home offensive stats
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

        print("Getting away stats . . .")
        away_rush_mets = pd.read_sql_query(away_rush_sql, kaggle_conn, index_col=None)
        away_rush_mets.set_index('game_id',inplace=True)
        away_short_pass_mets = pd.read_sql_query(away_short_pass_sql, kaggle_conn, index_col=None)
        away_short_pass_mets.set_index('game_id',inplace=True)
        away_deep_pass_mets = pd.read_sql_query(away_deep_pass_sql, kaggle_conn, index_col=None)
        away_deep_pass_mets.set_index('game_id',inplace=True)
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
        self.game_summary = gameinfo.merge(all_offense,on='game_id')

        return self.game_summary

    def get_skillpoints(self):
        print("Processing skillpoints per game . . .")

        game_summary_formatted = self.game_summary.copy().reset_index()
        sp = SkillPoints()
        self.skillpoints_df = sp.build_skillpoints_dataframe(game_summary_formatted)

        return self.skillpoints_df
