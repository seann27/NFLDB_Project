# import here
import pandas as pd

def calculate_home_rushFP(row):
    yards = row['home_rush_yds']
    ypa = yards/row['home_rush_att']
    tds = row['home_rush_tds']
    points = (yards/10)+(tds*6)+ypa
    return points

def calculate_away_rushFP(row):
    yards = row['away_rush_yds']
    ypa = yards/row['away_rush_att']
    tds = row['away_rush_tds']
    points = (yards/10)+(tds*6)+ypa
    return points

def calculate_home_passFP(row):
    yards = row['home_short_pass_yds']+row['home_deep_pass_yds']
    tds = row['home_pass_tds']
    completion_pct = row['home_completions']/row['home_pass_att']
    points = (yards/10)+(tds*6)+(row['home_completions']*completion_pct)-(row['home_interceptions']*2)-row['home_sacked']
    return points

def calculate_away_passFP(row):
    yards = row['away_short_pass_yds']+row['away_deep_pass_yds']
    tds = row['away_pass_tds']
    completion_pct = row['away_completions']/row['away_pass_att']
    points = (yards/10)+(tds*6)+(row['away_completions']*completion_pct)-(row['away_interceptions']*2)-row['away_sacked']
    return points

class SkillPoints():
	def __init__(self,gamestats):
		self.df = gamestats
		self.df['rush_skillpoints_home'] = self.df.apply (lambda row: calculate_home_rushFP(row), axis=1)
		self.df['rush_skillpoints_away'] = self.df.apply (lambda row: calculate_away_rushFP(row), axis=1)
		self.df['pass_skillpoints_home'] = self.df.apply (lambda row: calculate_home_passFP(row), axis=1)
		self.df['pass_skillpoints_away'] = self.df.apply (lambda row: calculate_away_passFP(row), axis=1)
