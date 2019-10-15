# import here
import pandas as pd
import numpy as np

# put this list into NFL_RefMaps package
skillpoint_cols = [
	'gameid',
	'team',
	'opponent',
	'rushing_skillpoints',
	'passing_skillpoints',
	'short_v_deep_pass_pct'
]

class SkillPoints():

	def __init__(self):
		self.skillpoints = pd.DataFrame(columns=skillpoint_cols)

	def build_skillpoints_dataframe(self,game_summary):
		skillpoints_by_team = []
		for game in game_summary.iterrows():
			skillpoints_by_team.append(get_team_skillpoints(game,'home'))
			skillpoints_by_team.append(get_team_skillpoints(game,'away'))

		skillpoints_df = np.vstack(skillpoints_by_team)
		self.skillpoints = pd.DataFrame(data=skillpoints_df,columns=skillpoint_cols)
		return self.skillpoints

	def get_team_skillpoints(row,side):
		team_stats = np.array([game['game_id']])
		side_team = side+"_team"
		side_opp = 'away_team'
		if side == 'away':
			side_opp = 'home_team'
		team = game[side_team]
		team_stats = np.append(team_stats,team)
		opponent = game[side_opp]
		team_stats = np.append(team_stats,opponent)
		rushing_skillpoints = calculate_rush_FP(game,side)
		team_stats = np.append(team_stats,rushing_skillpoints)
		passing_skillpoints,short_v_deep_pass_pct = calculate_passFP(game,side)
		team_stats = np.append(team_stats,passing_skillpoints)
		team_stats = np.append(team_stats,short_v_deep_pass_pct)
		return team_stats

	def calculate_rushFP(row,side):
        met_yds = side+"_rush_yds"
        met_att = side+"_rush_att"
        met_tds = side+"_rush_tds"
        yards = row[met_yds]
        ypa = yards/row[met_att]
        tds = row[met_tds]
        points = (yards/10)+(tds*6)+ypa
        return points

    def calculate_passFP(row,side):
		# short pass cols
		met_sp_yds = side+"_shortpass_yds"
		met_sp_att = side+"_shortpass_att"
		met_sp_comp = side+"_shortpass_completions"
		met_sp_tds = side+"_shortpass_tds"

		# short pass fp
        sp_yards = row[met_sp_yds]
        sp_tds = row[met_sp_tds]
        sp_completion_pct = row[met_sp_comp]/row[met_sp_att]
        sp_points = (sp_yards/10)+(sp_tds*6)+(row[met_sp_comp]*sp_completion_pct)

		# deep pass cols
		met_dp_yds = side+"_deeppass_yds"
		met_dp_att = side+"_deeppass_att"
		met_dp_comp = side+"_deeppass_completions"
		met_dp_tds = side+"_deeppass_tds"

		# deep pass fp
        dp_yards = row[met_dp_yds]
        dp_tds = row[met_dp_tds]
        dp_completion_pct = row[met_dp_comp]/row[met_dp_att]
        dp_points = (dp_yards/10)+(dp_tds*6)+(row[met_dp_comp]*dp_completion_pct)

		# calculate percentage short vs deep
		short_deep_pct = sp_points/dp_points

		# calculate total pass fp
		met_int = side+"_interceptions"
		met_sack = side+"_sacked"
		return (sp_points+dp_points-(row[met_int]*2)-row[met_sack]),short_deep_pct
