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

# initialize database sql engines
nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
main_engine = nfldb_engine.connect()

# scrape play by play from API for week
api_games = ApiGameLinks(season,week)
gameids = api_games.get_gameids()
pbp_df = pd.DataFrame(columns=TableColumns().nflapi['pbp_cols'])
for game in gameids:
    pbp = NFLAPI_Processor(game)
    pbp_df = pd.concat([pbp_df,pbp],verify_integrity=True)

# commit play-by-play dataframe to temp table
pbp_df.to_sql('nfl_pbp_temp', con=main_engine, if_exists='replace')

# generate game summaries
gs = GameSummary(season,week)
game_summary = gs.get_summary()
# generate skillpoint and performance metrics
skillpoints = gs.get_skillpoints()


# generate individual stats
# scrape new player data from pro-football-reference.com

# generate next week's preview metrics

# scrape fantasy pros projections
proj = LoadProjections(week).get_all_projections
for key,val in proj.items():
    table = 'week_'+str(week)+'_'+key+'_projections'
    val.to_sql(table, con=main_engine, if_exists='append')

# scrape fantasy pros rankings
rank = LoadRankings(week).get_all_rankings
for key,val in rank.items():
    table = 'week_'+str(week)+'_'+key+'_rankings'
    val.to_sql(table, con=main_engine, if_exists='append')

# scrape DFS salaries

# generate optimial lineups

# use ML to pick best lineups

# use ML to pick ATS, O/U results

### TO DO ###
# edit the metrics package so that skillpoints can be calculated individually?
#   -> can this already be used, but use player stats as input?
