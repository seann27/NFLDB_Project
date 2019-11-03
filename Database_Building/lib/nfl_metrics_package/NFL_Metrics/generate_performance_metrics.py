# import here
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# connect to database
nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
main_engine = nfldb_engine.connect()

get_games_sql = "select av from nfl_skillpoints \
				 	where "
