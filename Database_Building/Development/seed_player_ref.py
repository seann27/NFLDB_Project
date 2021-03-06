import pandas as pd
from sqlalchemy import engine

nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
main_engine = nfldb_engine.connect()

# will need to store in table columns package eventually
cols = ['nflapi_id','pfr_id','first_name','last_name','position','team']

sql = """
select pid,name,team from (
select distinct(passer_player_id) as pid, passer_player_name as name, posteam as team from nfl_pbp
union
select distinct(rusher_player_id) as pid, rusher_player_name as name, posteam as team from nfl_pbp
union
select distinct(receiver_player_id) as pid, receiver_player_name as name, posteam as team from nfl_pbp
union
select distinct(kicker_player_id) as pid, kicker_player_name as name, posteam as team from nfl_pbp
union
select distinct(tackle_for_loss_1_player_id) as pid, tackle_for_loss_1_player_name as name, case when home_team = posteam then away_team else home_team end as team from nfl_pbp
union
select distinct(pass_defense_1_player_id) as pid, pass_defense_1_player_name as name, case when home_team = posteam then away_team else home_team end as team from nfl_pbp
) as player_query
where pid is not null
and name is not null
and team is not null
"""

df = pd.read_sql(sql,con=main_engine)

players = pd.DataFrame(columns=cols)
players['nflapi_id'] = df['pid']

def get_name(row,type):
    name_comps = row['name'].split('.')
    first = name_comps[0].strip()
    last = name_comps[1].strip()
    if type == 'first':
        return first
    else:
        return last

players['first_name'] = df.apply(lambda row: get_name('first'),axis=1)
players['last_name'] = df.apply(lambda row: get_name('last'),axis=1)

players.drop_duplicates(inplace=True,subset='nflapi_id',keep='last')

players.to_sql('nfl_player_db',con=main_engine,if_exists='replace')
