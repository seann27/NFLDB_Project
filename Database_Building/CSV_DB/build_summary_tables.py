import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql://root:@localhost:3306/nfl_db')

# get all players with rushing stats
rush_sql = "select distinct concat(game_id,rusher_player_id) as sid,rusher_player_name, posteam, sum(fumble_lost) from nfl_pbp where play_type='run' group by sid order by sid"
rush_df = pd.read_sql(sql=rush_sql,index_col=sid)
rush_detailed_sql = "select concat(game_id,rusher_player_id) as sid,rusher_player_name,posteam,sum(rush_attempt), sum(yards_gained), sum(rush_touchdown) from nfl_pbp where play_type='run' and run_location=%(loc)s and run_gap=%(gap)s group by sid"

def append_rush_directions(df,loc,gap):
	detailed_df = pd.read_sql(sql=rush_detailed_sql,con=engine,index_col=sid,params={'loc':loc,'gap':gap})
	# join detailed_df with df
	# return df

rush_df = append_rush_directions(rush_df,'left','end')
rush_df = append_rush_directions(rush_df,'left','tackle')
rush_df = append_rush_directions(rush_df,'left','guard')
rush_df = append_rush_directions(rush_df,'middle',null)
rush_df = append_rush_directions(rush_df,'right','end')
rush_df = append_rush_directions(rush_df,'right','tackle')
rush_df = append_rush_directions(rush_df,'right','guard')

# get all players with passing/receiving stats
