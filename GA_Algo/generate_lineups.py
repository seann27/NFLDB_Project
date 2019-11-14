# import here
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import random
from pyeasyga import pyeasyga
from random import shuffle
import time

start = time.time()

# connect to database
nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
main_engine = nfldb_engine.connect()

# get player sql
