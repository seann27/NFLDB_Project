# imports
import pandas as pd
import sys
import argparse
from NFL_Dataloader import GameSummary,NFLAPI_Processor
from scrapers import ApiGameLinks
from NFL_RefMaps import TableColumns
from NFL_Metrics import SkillPoints

# get arguments
parser = argparse.ArgumentParser()
parser.add_argument("--season", help="NFL season")
parser.add_argument("--week", help="NFL week (regular season)")
args = parser.parse_args()
season = args.season
week = args.week
table_updates = {}

# initialize database sql engines
nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/nfl_db')
conn = nfldb_engine.connect()

def update_table(table,temp_table):
    sql = "REPLACE INTO "+table
    sql += " (select * from "+temp_table+")"

def check_table(conn,table):
	sql = '''SELECT COUNT(*)
	    FROM information_schema.tables
	    WHERE table_name = '{}'
	    '''.format(table)
	result = conn.execute(sql)
	return True if result.fetchone()[0] == 1 else False

def remove_tmp_tables(conn):
    sql = '''SELECT table_name
            FROM information_schema.tables
            WHERE table_name like '%%_tmp'
            '''

    result = conn.execute(sql)
    for row in result:
        conn.execute('DROP TABLE IF EXISTS %s'%row[0])

def load_fp(dict,type):
    for key,val in dict.items():
        table = key + '_' + type
        temp = table + '_temp'
        table_updates[table] = temp
        val.to_sql(temp, con=main_engine, if_exists='replace')

def load_fp_metrics(data,metric,week):
    prefix = 'fpros_'
    for key,val in data.items():
        table = prefix+key+'_'+metric
        tmp = table+'_tmp'
        if check_table(conn,table):
            val.to_sql(tmp, con=conn, if_exists='replace',dtype={'idx': VARCHAR(val.index.get_level_values('idx').str.len().max())})
            update_table(conn,table,tmp)
        else:
            val.to_sql(table, con=conn, if_exists='replace',dtype={'idx': VARCHAR(val.index.get_level_values('idx').str.len().max())})

# scrape play by play from API for week
api_games = ApiGameLinks(season,week)
gameids = api_games.get_gameids()
pbp_df = pd.DataFrame(columns=TableColumns().nflapi['pbp_cols'])
for game in gameids:
    pbp = NFLAPI_Processor(game)
    pbp_df = pd.concat([pbp_df,pbp],verify_integrity=True)
pbp_df.to_sql('nfl_pbp_tmp', con=conn, if_exists='replace')
update_table('nfl_pbp','nfl_pbp_tmp')

# generate game summaries
gs = GameSummary(season,week)
game_summary = gs.get_summary()
skillpoints = gs.get_skillpoints()
game_summary.to_sql('nfl_game_summary_tmp', con=conn, if_exists='replace',index='gameid')
update_table('nfl_game_summary','nfl_game_summary_tmp')
skillpoints.to_sql('nfl_team_skillpoints_tmp', con=conn, if_exists='replace',index='idx')
update_table('nfl_team_skillpoints','nfl_team_skillpoints_tmp')

# scrape final fantasy pros projections and rankings
load_fp(LoadProjections(week).projections,'projections')
load_fp(LoadRankings(week).rankings,'rankings')

# generate individual stats

# scrape new player data from pro-football-reference.com

# generate next week's preview metrics

# update tables
for key,val in table_updates.items():
    update_table(key,val)

# scrape DFS salaries

# generate optimial lineups

# use ML to pick best lineups

# use ML to pick ATS, O/U results

### TO DO ###
# edit the metrics package so that skillpoints can be calculated individually?
#   -> can this already be used, but use player stats as input?
