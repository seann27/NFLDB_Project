# import here
import pandas as pd
from sqlalchemy import create_engine
from references_dict import Team_Dictionary
from calculate_skillpoints import SkillPoints

# connect to databases
print("Seeding gamestats . . .")
kaggle_engine = create_engine('mysql+pymysql://root:@localhost:3306/kaggle')
kaggle_conn = kaggle_engine.connect()
main_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
main_conn = main_engine.connect()

# home stats
home_rush_sql = "select game_id, posteam as home_abbrev, sum(yards_gained) as home_rush_yds, sum(rush_attempt) as home_rush_att,sum(rush_touchdown) as home_rush_tds \
  from nfl_pbp \
  where posteam = home_team \
  and play_type = 'run' \
group by game_id"

home_short_pass_sql = "select game_id,sum(yards_gained) as home_short_pass_yds \
  from nfl_pbp \
  where play_type='pass' \
  and pass_length = 'short' \
  and posteam=home_team \
  group by game_id,posteam"

home_deep_pass_sql = "select game_id,sum(yards_gained) as home_deep_pass_yds \
  from nfl_pbp \
  where play_type='pass' \
  and pass_length = 'deep' \
  and posteam=home_team \
  group by game_id,posteam"

home_pass_total_sql = "select game_id, \
       sum(pass_attempt) as home_pass_att, \
       sum(complete_pass) as home_completions, \
       sum(pass_touchdown) as home_pass_tds, \
       sum(sack) as home_sacked, \
       sum(interception) as home_interceptions \
  from nfl_pbp \
  where play_type = 'pass' \
  and posteam = home_team \
  group by game_id"

home_rush_mets = pd.read_sql_query(home_rush_sql, kaggle_conn, index_col=None)
home_rush_mets.set_index('game_id',inplace=True)
home_short_pass_mets = pd.read_sql_query(home_short_pass_sql, kaggle_conn, index_col=None)
home_short_pass_mets.set_index('game_id',inplace=True)
home_deep_pass_mets = pd.read_sql_query(home_deep_pass_sql, kaggle_conn, index_col=None)
home_deep_pass_mets.set_index('game_id',inplace=True)
home_pass_mets = pd.read_sql_query(home_pass_total_sql, kaggle_conn, index_col=None)
home_pass_mets.set_index('game_id',inplace=True)

home_offense = home_rush_mets.merge(home_short_pass_mets,on='game_id')
home_offense = home_offense.merge(home_deep_pass_mets,on='game_id')
home_offense = home_offense.merge(home_pass_mets,on='game_id')
print("Home stats generated.")

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

away_short_pass_sql = "select game_id,sum(yards_gained) as away_short_pass_yds \
  from nfl_pbp \
  where play_type='pass' \
  and pass_length = 'short' \
  and posteam = away_team \
  group by game_id,posteam"

away_deep_pass_sql = "select game_id,sum(yards_gained) as away_deep_pass_yds \
  from nfl_pbp \
  where play_type='pass' \
  and pass_length = 'deep' \
  and posteam = away_team \
  group by game_id,posteam"

away_pass_total_sql = "select game_id, \
       sum(pass_attempt) as away_pass_att, \
       sum(complete_pass) as away_completions, \
       sum(pass_touchdown) as away_pass_tds, \
       sum(sack) as away_sacked, \
       sum(interception) as away_interceptions \
  from nfl_pbp \
  where play_type = 'pass' \
  and posteam = away_team \
  group by game_id"

away_rush_mets = pd.read_sql_query(away_rush_sql, kaggle_conn, index_col=None)
away_rush_mets.set_index('game_id',inplace=True)
away_short_pass_mets = pd.read_sql_query(away_short_pass_sql, kaggle_conn, index_col=None)
away_short_pass_mets.set_index('game_id',inplace=True)
away_deep_pass_mets = pd.read_sql_query(away_deep_pass_sql, kaggle_conn, index_col=None)
away_deep_pass_mets.set_index('game_id',inplace=True)
away_pass_mets = pd.read_sql_query(away_pass_total_sql, kaggle_conn, index_col=None)
away_pass_mets.set_index('game_id',inplace=True)

away_offense = away_rush_mets.merge(away_short_pass_mets,on='game_id')
away_offense = away_offense.merge(away_deep_pass_mets,on='game_id')
away_offense = away_offense.merge(away_pass_mets,on='game_id')
print("Away stats generated.")

all_offense = home_offense.merge(away_offense,on='game_id')
df = SkillPoints(all_offense).df
print("Skill points generated.")
print("Generating table in database . . .")
df.to_sql('nfl_gamestats', con=main_engine, if_exists='replace',index='game_id')
