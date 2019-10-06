# import here
import pandas as pd
from sqlalchemy import create_engine
from references_dict import Team_Dictionary

# connect to database
print("Seeding gameinfo table . . .")
kaggle_engine = create_engine('mysql+pymysql://root:@localhost:3306/kaggle')
kaggle_conn = kaggle_engine.connect()
nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
nfldb_conn = nfldb_engine.connect()
file = ("D:\\NFLDB\\game_info.csv")

# trim csv file to relevant stats for weeks 1-16, 2009-2018
df = pd.read_csv(file)

# drop playoff weeks
indexNames = df[ df['schedule_playoff'] == True ].index
df.drop(indexNames,inplace=True)

# drop stats older than 2009
indexNames = df[ df['schedule_season'] < 2009 ].index
df.drop(indexNames,inplace=True)

# drop unused columns
df.drop(['schedule_playoff'],axis=1,inplace=True)
df.drop(['stadium'],axis=1,inplace=True)
df.drop(['stadium_neutral'],axis=1,inplace=True)
df.drop(['weather_temperature'],axis=1,inplace=True)
df.drop(['weather_wind_mph'],axis=1,inplace=True)
df.drop(['weather_humidity'],axis=1,inplace=True)
df.drop(['weather_detail'],axis=1,inplace=True)

def get_home_favorite(row):
	home_team = row['team_home']
	home_abbrev = Team_Dictionary().kaggle_games_abbrev[home_team]
	if home_abbrev == row['team_favorite_id']:
		return 1
	else:
		return 0

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
    return date+Team_Dictionary().kaggle_games_abbrev[row['team_home']]

# # generate metrics for dataset, set index
print("Generating odds metrics for gameinfo table . . .")
df['home_favorite'] = df.apply (lambda row: get_home_favorite(row), axis=1)
df['spread_result'] = df.apply(lambda row: get_spread_result(row),axis=1)
df['OU_result'] = df.apply(lambda row: get_OU_result(row),axis=1)
df['idx'] = df.apply(lambda row: get_index(row),axis=1)
df.set_index('idx',inplace=True)

def get_pbpindex(row):
    team_dict = dict([[v,k] for k,v in Team_Dictionary().kaggle_plays_abbrev.items()])
    team_name = team_dict[row['home_team']]
    team_name = Team_Dictionary().kaggle_games_abbrev[team_name]
    comps = row['game_date'].split('/')
    date = comps[2]+'-'+str(comps[0]).zfill(2)+'-'+str(comps[1]).zfill(2)
    idx = date+team_name
    return idx

# sql statement for getting gameids
sql = "select distinct(pbp.game_id) as game_id, pbp.home_team as home_team, pbp.game_date as game_date \
       from nfl_pbp pbp \
       order by pbp.game_id"
df_gameids = pd.read_sql_query(sql, kaggle_conn, index_col=None)
df_gameids['idx'] = df_gameids.apply(lambda row: get_pbpindex(row),axis=1)

df_gameids.set_index('idx',inplace=True)
df['game_id']=df_gameids['game_id']
df.set_index('game_id',inplace=True)
print("Creating and inserting gameinfo table . . .")
df.to_sql('nfl_gameinfo', con=nfldb_engine, if_exists='replace',index='game_id')
