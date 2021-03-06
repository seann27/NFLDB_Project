# import here
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

class TeamPerformance:

	def __init__(self,season,week,skillpoint_dict):
		self.season = season
		self.week = week
		self.skillpoint_dict = skillpoint_dict

		# connect to database
		nfldb_engine = create_engine('mysql+pymysql://root:@localhost:3306/nfl_db')
		self.conn = nfldb_engine.connect()

	def get_performance_mets(self,metric,team,opp):
		base_sql = "select avg("+metric+") as avg_"+metric+" from nfl_skillpoints "
		base_suffix = " and season = :season and week < :week"
		team_avg_sql = base_sql + "where team = :team " + base_suffix
		opp_avg_sql = base_sql + "where opponent = :opp " + base_suffix

		params = {
			'team' : team,
			'opp' : opp,
			'season' : self.season,
			'week' : self.week
		}

		skillpoints = self.skillpoint_dict[metric]
		team_avg = self.conn.execute(team_avg_sql,params=params).fetchone()
		opp_avg = self.conn.execute(opp_avg_sql,params=params).fetchone()
		performance = (skillpoints**2)/(team_avg*opp_avg)
		return performance

	def get_team_performance(self,team,opp):
		rush = self.get_performance_mets('rushing_skillpoints',team,opp)
		sp = self.get_performance_mets('short_pass_skillpoints',team,opp)
		dp = self.get_performance_mets('deep_pass_skillpoints',team,opp)
		return rush,sp,dp
