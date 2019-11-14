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

class GameSummary:

    def __init__(self,season,week):
        self.season = season
        self.week = week

    def get_summary():
        gamelinks = PFR_Gamelinks.get_game_links(self.season,self.week)
        for link in gamelinks:
            game = PFR_Gamepage(link)
            gameinfo = game.get_gameinfo()
