# import here
import pandas as pd
import numpy as np
from generate_performance_metrics import TeamPerformance

# put this list into NFL_RefMaps package
skillpoint_cols = [
	'gameid',
	'team',
	'opponent',
	'rushing_skillpoints',
	'short_pass_skillpoints',
	'deep_pass_skillpoints',
	'rush_performance',
	'short_pass_performance',
	'deep_pass_performance'
]

def get_team_skillpoints(game,side):
	team_stats = [int(game['game_id'])]
	side_team = "team_"+side
	side_opp = 'team_away'
	if side == 'away':
		side_opp = 'team_home'
	team = game[side_team]
	team_stats.append(team)
	opponent = game[side_opp]
	team_stats.append(opponent)
	rushing_skillpoints = calculate_rushFP(game,side)
	team_stats.append(rushing_skillpoints)
	passing_skillpoints,short_pct,deep_pct = calculate_passFP(game,side)
	team_stats.append(passing_skillpoints)
	team_stats.append(short_pct)
	team_stats.append(deep_pct)
	performance = TeamPerformance(game['season'],game['week'])
	rush,sp,dp = performance.get_team_performance(team,opponent)
	team_stats.append(rush)
	team_stats.append(sp)
	team_stats.append(dp)
	team_stats = np.asarray(team_stats)
	return team_stats

def calculate_rushFP(game,side):
	met_yds = side+"_rush_yds"
	met_att = side+"_rush_att"
	met_tds = side+"_rush_tds"
	yards = game[met_yds]
	ypa = yards/game[met_att]
	tds = game[met_tds]
	points = (yards/10)+(tds*6)+ypa
	return points

def calculate_passFP(game,side):
	# short pass cols
	met_sp_yds = side+"_shortpass_yds"
	met_sp_att = side+"_shortpass_att"
	met_sp_comp = side+"_shortpass_completions"
	met_sp_tds = side+"_shortpass_tds"
	met_sp_int = side+"_short_interceptions"

	# short pass fp
	sp_yards = game[met_sp_yds]
	sp_tds = game[met_sp_tds]
	sp_completion_pct = game[met_sp_comp]/game[met_sp_att]
	sp_points = (sp_yards/10)+(sp_tds*6)+(game[met_sp_comp]*sp_completion_pct)-(game[met_sp_int]*2)

	# deep pass cols
	met_dp_yds = side+"_deeppass_yds"
	met_dp_att = side+"_deeppass_att"
	met_dp_comp = side+"_deeppass_completions"
	met_dp_tds = side+"_deeppass_tds"
	met_dp_int = side+"_deep_interceptions"

	# deep pass fp
	dp_yards = game[met_dp_yds]
	dp_tds = game[met_dp_tds]
	dp_completion_pct = game[met_dp_comp]/game[met_dp_att]
	dp_points = (dp_yards/10)+(dp_tds*6)+(game[met_dp_comp]*dp_completion_pct)-(game[met_dp_int]*2)

	# calculate total pass fp
	met_sack = side+"_sacked"
	return (sp_points+dp_points-game[met_sack])


class SkillPoints():

	def __init__(self):
		self.skillpoints = pd.DataFrame(columns=skillpoint_cols)

	def build_skillpoints_dataframe(self,game_summary):
		skillpoints_by_team = []
		for index,game in game_summary.iterrows():
			skillpoints_by_team.append(get_team_skillpoints(game,'home'))
			skillpoints_by_team.append(get_team_skillpoints(game,'away'))

		skillpoints_df = np.vstack(skillpoints_by_team)
		self.skillpoints = pd.DataFrame(data=skillpoints_df,columns=skillpoint_cols)
		return self.skillpoints
