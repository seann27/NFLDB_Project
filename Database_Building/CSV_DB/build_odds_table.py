import pandas as pd
from sqlalchemy import create_engine
from references_dict import Team_Dictionary
engine = create_engine('mysql://root:@localhost:3306/nfl_db')
file = ("D:\\NFLDB\\game_info.csv")
df = pd.read_csv(file)
df.to_sql('nfl_pbp', con=engine, if_exists=action,index=False)
