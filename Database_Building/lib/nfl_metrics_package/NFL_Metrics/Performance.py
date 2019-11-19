# import here
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

class TeamPerformance:

	def __init__(self,season,week):
		self.season = season
		self.week = week

		# connect to database
		nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/main_stats')
		self.main_engine = nfldb_engine.connect()

	def get_performance_mets(self,metric,team,opp):
		sp_sql = "select "+metric+" from nfl_skillpoints "
		sp_sql += " where team = :team and season = :season and week = :week"

		base_sql = "select avg("+metric+") as avg_"+metric+" from nfl_skillpoints "
		base_suffix += " and season = :season and week < :week"
		team_avg_sql = base_sql + "where team = :team " + base_suffix
		opp_avg_sql = base_sql + "where opponent = :opp " + base_suffix

		params = {
			'team' : team,
			'opp' : opp,
			'season' : self.season,
			'week' : self.week
		}

		skillpoints = self.main_engine.execute(sp_sql,params=params).fetchone()
		team_avg = self.main_engine.execute(team_avg_sql,params=params).fetchone()
		opp_avg = self.main_engine.execute(opp_avg_sql,params=params).fetchone()
		performance = (skillpoints**2)/(team_avg*opp_avg)
		return performance

	def get_team_performance(self,team,opp):
		rush = get_performance_mets('rushing_skillpoints',team,opp)
		sp = get_performance_mets('short_pass_skillpoints',team,opp)
		dp = get_performance_mets('deep_pass_skillpoints',team,opp)
		return rush,sp,dp
