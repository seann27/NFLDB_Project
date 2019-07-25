import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql://root:@localhost:3306/nfl_db')
# https://www.kaggle.com/maxhorowitz/nflplaybyplay2009to2016
# https://github.com/maksimhorowitz/nflscrapR/blob/master/R/scrape_play_by_play.R
dbint = 'int64'
dbstring = 'str'
dbfloat = 'float64'
dbdatetime = 'str'
dtypes = {
	'play_id':dbint,
	'game_id':dbint,
	'home_team':dbstring,
	'away_team':dbstring,
	'posteam':dbstring,
	'posteam_type':dbstring,
	'defteam':dbstring,
	'side_of_field':dbstring,
	'yardline_100':dbstring,
	'game_date':dbdatetime,
	'quarter_seconds_remaining':dbfloat,
	'half_seconds_remaining':dbfloat,
	'game_seconds_remaining':dbfloat,
	'game_half':dbstring,
	'quarter_end':dbint,
	'drive':dbint,
	'sp':dbint,
	'qtr':dbint,
	'down':dbstring,
	'goal_to_go':dbstring,
	'time':dbdatetime,
	'yrdln':dbstring,
	'ydstogo':dbint,
	'ydsnet':dbint,
	'desc':dbstring,
	'play_type':dbstring,
	'yards_gained':dbfloat,
	'shotgun':dbint,
	'no_huddle':dbint,
	'qb_dropback':dbstring,
	'qb_kneel':dbint,
	'qb_spike':dbint,
	'qb_scramble':dbint,
	'pass_length':dbstring,
	'pass_location':dbstring,
	'air_yards':dbstring,
	'yards_after_catch':dbstring,
	'run_location':dbstring,
	'run_gap':dbstring,
	'field_goal_result':dbstring,
	'kick_distance':dbstring,
	'extra_point_result':dbstring,
	'two_point_conv_result':dbstring,
	'home_timeouts_remaining':dbint,
	'away_timeouts_remaining':dbint,
	'timeout':dbstring,
	'timeout_team':dbstring,
	'td_team':dbstring,
	'posteam_timeouts_remaining':dbstring,
	'defteam_timeouts_remaining':dbstring,
	'total_home_score':dbint,
	'total_away_score':dbint,
	'posteam_score':dbstring,
	'defteam_score':dbstring,
	'score_differential':dbstring,
	'posteam_score_post':dbstring,
	'defteam_score_post':dbstring,
	'score_differential_post':dbstring,
	'no_score_prob':dbfloat,
	'opp_fg_prob':dbfloat,
	'opp_safety_prob':dbfloat,
	'opp_td_prob':dbfloat,
	'fg_prob':dbfloat,
	'safety_prob':dbfloat,
	'td_prob':dbfloat,
	'extra_point_prob':dbfloat,
	'two_point_conversion_prob':dbfloat,
	'ep':dbstring,
	'epa':dbstring,
	'total_home_epa':dbfloat,
	'total_away_epa':dbfloat,
	'total_home_rush_epa':dbfloat,
	'total_away_rush_epa':dbfloat,
	'total_home_pass_epa':dbfloat,
	'total_away_pass_epa':dbfloat,
	'air_epa':dbstring,
	'yac_epa':dbstring,
	'comp_air_epa':dbstring,
	'comp_yac_epa':dbstring,
	'total_home_comp_air_epa':dbfloat,
	'total_away_comp_air_epa':dbfloat,
	'total_home_comp_yac_epa':dbfloat,
	'total_away_comp_yac_epa':dbfloat,
	'total_home_raw_air_epa':dbfloat,
	'total_away_raw_air_epa':dbfloat,
	'total_home_raw_yac_epa':dbfloat,
	'total_away_raw_yac_epa':dbfloat,
	'wp':dbstring,
	'def_wp':dbstring,
	'home_wp':dbstring,
	'away_wp':dbstring,
	'wpa':dbstring,
	'home_wp_post':dbstring,
	'away_wp_post':dbstring,
	'total_home_rush_wpa':dbfloat,
	'total_away_rush_wpa':dbfloat,
	'total_home_pass_wpa':dbfloat,
	'total_away_pass_wpa':dbfloat,
	'air_wpa':dbstring,
	'yac_wpa':dbstring,
	'comp_air_wpa':dbstring,
	'comp_yac_wpa':dbstring,
	'total_home_comp_air_wpa':dbfloat,
	'total_away_comp_air_wpa':dbfloat,
	'total_home_comp_yac_wpa':dbfloat,
	'total_away_comp_yac_wpa':dbfloat,
	'total_home_raw_air_wpa':dbfloat,
	'total_away_raw_air_wpa':dbfloat,
	'total_home_raw_yac_wpa':dbfloat,
	'total_away_raw_yac_wpa':dbfloat,
	'punt_blocked':dbstring,
	'first_down_rush':dbstring,
	'first_down_pass':dbstring,
	'first_down_penalty':dbstring,
	'third_down_converted':dbstring,
	'third_down_failed':dbstring,
	'fourth_down_converted':dbstring,
	'fourth_down_failed':dbstring,
	'incomplete_pass':dbstring,
	'interception':dbstring,
	'punt_inside_twenty':dbstring,
	'punt_in_endzone':dbstring,
	'punt_out_of_bounds':dbstring,
	'punt_downed':dbstring,
	'punt_fair_catch':dbstring,
	'kickoff_inside_twenty':dbstring,
	'kickoff_in_endzone':dbstring,
	'kickoff_out_of_bounds':dbstring,
	'kickoff_downed':dbstring,
	'kickoff_fair_catch':dbstring,
	'fumble_forced':dbstring,
	'fumble_not_forced':dbstring,
	'fumble_out_of_bounds':dbstring,
	'solo_tackle':dbstring,
	'safety':dbstring,
	'penalty':dbstring,
	'tackled_for_loss':dbstring,
	'fumble_lost':dbstring,
	'own_kickoff_recovery':dbstring,
	'own_kickoff_recovery_td':dbstring,
	'qb_hit':dbstring,
	'rush_attempt':dbstring,
	'pass_attempt':dbstring,
	'sack':dbstring,
	'touchdown':dbstring,
	'pass_touchdown':dbstring,
	'rush_touchdown':dbstring,
	'return_touchdown':dbstring,
	'extra_point_attempt':dbstring,
	'two_point_attempt':dbstring,
	'field_goal_attempt':dbstring,
	'kickoff_attempt':dbstring,
	'punt_attempt':dbstring,
	'fumble':dbstring,
	'complete_pass':dbstring,
	'assist_tackle':dbstring,
	'lateral_reception':dbstring,
	'lateral_rush':dbstring,
	'lateral_return':dbstring,
	'lateral_recovery':dbstring,
	'passer_player_id':dbstring,
	'passer_player_name':dbstring,
	'receiver_player_id':dbstring,
	'receiver_player_name':dbstring,
	'rusher_player_id':dbstring,
	'rusher_player_name':dbstring,
	'lateral_receiver_player_id':dbstring,
	'lateral_receiver_player_name':dbstring,
	'lateral_rusher_player_id':dbstring,
	'lateral_rusher_player_name':dbstring,
	'lateral_sack_player_id':dbstring,
	'lateral_sack_player_name':dbstring,
	'interception_player_id':dbstring,
	'interception_player_name':dbstring,
	'lateral_interception_player_id':dbstring,
	'lateral_interception_player_name':dbstring,
	'punt_returner_player_id':dbstring,
	'punt_returner_player_name':dbstring,
	'lateral_punt_returner_player_id':dbstring,
	'lateral_punt_returner_player_name':dbstring,
	'kickoff_returner_player_name':dbstring,
	'kickoff_returner_player_id':dbstring,
	'lateral_kickoff_returner_player_id':dbstring,
	'lateral_kickoff_returner_player_name':dbstring,
	'punter_player_id':dbstring,
	'punter_player_name':dbstring,
	'kicker_player_name':dbstring,
	'kicker_player_id':dbstring,
	'own_kickoff_recovery_player_id':dbstring,
	'own_kickoff_recovery_player_name':dbstring,
	'blocked_player_id':dbstring,
	'blocked_player_name':dbstring,
	'tackle_for_loss_1_player_id':dbstring,
	'tackle_for_loss_1_player_name':dbstring,
	'tackle_for_loss_2_player_id':dbstring,
	'tackle_for_loss_2_player_name':dbstring,
	'qb_hit_1_player_id':dbstring,
	'qb_hit_1_player_name':dbstring,
	'qb_hit_2_player_id':dbstring,
	'qb_hit_2_player_name':dbstring,
	'forced_fumble_player_1_team':dbstring,
	'forced_fumble_player_1_player_id':dbstring,
	'forced_fumble_player_1_player_name':dbstring,
	'forced_fumble_player_2_team':dbstring,
	'forced_fumble_player_2_player_id':dbstring,
	'forced_fumble_player_2_player_name':dbstring,
	'solo_tackle_1_team':dbstring,
	'solo_tackle_2_team':dbstring,
	'solo_tackle_1_player_id':dbstring,
	'solo_tackle_2_player_id':dbstring,
	'solo_tackle_1_player_name':dbstring,
	'solo_tackle_2_player_name':dbstring,
	'assist_tackle_1_player_id':dbstring,
	'assist_tackle_1_player_name':dbstring,
	'assist_tackle_1_team':dbstring,
	'assist_tackle_2_player_id':dbstring,
	'assist_tackle_2_player_name':dbstring,
	'assist_tackle_2_team':dbstring,
	'assist_tackle_3_player_id':dbstring,
	'assist_tackle_3_player_name':dbstring,
	'assist_tackle_3_team':dbstring,
	'assist_tackle_4_player_id':dbstring,
	'assist_tackle_4_player_name':dbstring,
	'assist_tackle_4_team':dbstring,
	'pass_defense_1_player_id':dbstring,
	'pass_defense_1_player_name':dbstring,
	'pass_defense_2_player_id':dbstring,
	'pass_defense_2_player_name':dbstring,
	'fumbled_1_team':dbstring,
	'fumbled_1_player_id':dbstring,
	'fumbled_1_player_name':dbstring,
	'fumbled_2_player_id':dbstring,
	'fumbled_2_player_name':dbstring,
	'fumbled_2_team':dbstring,
	'fumble_recovery_1_team':dbstring,
	'fumble_recovery_1_yards':dbstring,
	'fumble_recovery_1_player_id':dbstring,
	'fumble_recovery_1_player_name':dbstring,
	'fumble_recovery_2_team':dbstring,
	'fumble_recovery_2_yards':dbstring,
	'fumble_recovery_2_player_id':dbstring,
	'fumble_recovery_2_player_name':dbstring,
	'return_team':dbstring,
	'return_yards':dbfloat,
	'penalty_team':dbstring,
	'penalty_player_id':dbstring,
	'penalty_player_name':dbstring,
	'penalty_yards':dbstring,
	'replay_or_challenge':dbfloat,
	'replay_or_challenge_result':dbstring,
	'penalty_type':dbstring,
	'defensive_two_point_attempt':dbstring,
	'defensive_two_point_conv':dbstring,
	'defensive_extra_point_attempt':dbstring,
	'defensive_extra_point_conv':dbstring
}

cols = [
	'play_id', # Numeric play id that when used with game_id and drive provides
	'game_id', # Ten digit identifier for NFL game.
	'home_team', # String abbreviation for the home team.
	'away_team', # String abbreviation for the away team.
	'posteam', # String abbreviation for the team with possession.
	'yardline_100', # Numeric distance in the number of yards from the opponent's endzone for the posteam.
	'game_date', # Date of the game.
	'quarter_end', # Binary indicator for whether or not the row of the data is marking the end of a quarter.
	'drive', # Numeric drive number in the game.
	'sp', # Binary indicator for whether or not a score occurred on the play.
	'qtr', # Quarter of the game (5 is overtime).
	'down', # The down for the given play.
	'goal_to_go', # Binary indicator for whether or not the posteam is in a goal down situation.
	'ydstogo', # Numeric yards in distance from either the first down marker or the endzone in goal down situations.
	'ydsnet', # Numeric value for total yards gained on the given drive.
	'desc', # Detailed string description for the given play.
	'play_type', # String indicating the type of play: pass (includes sacks),  run (includes scrambles), punt, field_goal, kickoff, extra_point,  qb_kneel, qb_spike, no_play (timeouts and penalties), and missing for rows indicating end of play.
	'yards_gained', # Numeric yards gained (or lost) for the given play.
	'shotgun', # Binary indicator for whether or not the play was in shotgun formation.
	'no_huddle', # Binary indicator for whether or not the play was in no_huddle formation.
	'qb_dropback', # Binary indicator for whether or not the QB dropped back on the play (pass attempt, sack, or scrambled).
	'qb_scramble', # Binary indicator for whether or not the QB scrambled.
	'pass_length', # String indicator for pass length: short or deep.
	'pass_location', # String indicator for pass location: left, middle, or right.
	'air_yards', # Numeric value for distance in yards perpendicular to the line of scrimmage at where the targeted receiver either caught or didn't catch the ball.
	'yards_after_catch', # Numeric value for distance in yards perpendicular to the yard line where the receiver made the reception to where the play ended.
	'run_location', # String indicator for location of run: left, middle, or right.
	'run_gap', # String indicator for line gap of run: end, guard, or tackle
	'field_goal_result', # String indicator for result of field goal attempt: made, missed, or blocked.
	'kick_distance', # Numeric distance in yards for kickoffs, field goals, and punts.
	'extra_point_result', # String indicator for the result of the extra point attempt: good, failed, blocked, safety (touchback in defensive endzone is 1 point apparently), or aborted.
	'two_point_conv_result',
	'timeout',
	'timeout_team',
	'td_team',
	'posteam_timeouts_remaining',
	'defteam_timeouts_remaining',
	'total_home_score',
	'total_away_score',
	'posteam_score',
	'defteam_score',
	'score_differential',
	'posteam_score_post',
	'defteam_score_post',
	'score_differential_post',
	'punt_blocked',
	'incomplete_pass',
	'interception',
	'kickoff_inside_twenty',
	'kickoff_in_endzone',
	'kickoff_out_of_bounds',
	'kickoff_downed',
	'kickoff_fair_catch',
	'fumble_forced',
	'fumble_not_forced',
	'fumble_out_of_bounds',
	'safety',
	'penalty',
	'tackled_for_loss',
	'fumble_lost',
	'qb_hit',
	'rush_attempt',
	'pass_attempt',
	'sack',
	'touchdown',
	'pass_touchdown',
	'rush_touchdown',
	'return_touchdown',
	'extra_point_attempt',
	'two_point_attempt',
	'field_goal_attempt',
	'kickoff_attempt',
	'punt_attempt',
	'fumble',
	'complete_pass',
	'passer_player_id',
	'passer_player_name',
	'receiver_player_id',
	'receiver_player_name',
	'rusher_player_id',
	'rusher_player_name',
	'interception_player_id',
	'interception_player_name',
	'punt_returner_player_id',
	'punt_returner_player_name',
	'kickoff_returner_player_name',
	'kickoff_returner_player_id',
	'punter_player_id',
	'punter_player_name',
	'kicker_player_name',
	'kicker_player_id',
	'blocked_player_id',
	'blocked_player_name',
	'tackle_for_loss_1_player_id',
	'tackle_for_loss_1_player_name',
	'tackle_for_loss_2_player_id',
	'tackle_for_loss_2_player_name',
	'qb_hit_1_player_id',
	'qb_hit_1_player_name',
	'qb_hit_2_player_id',
	'qb_hit_2_player_name',
	'forced_fumble_player_1_team',
	'forced_fumble_player_1_player_id',
	'forced_fumble_player_1_player_name',
	'forced_fumble_player_2_team',
	'forced_fumble_player_2_player_id',
	'forced_fumble_player_2_player_name',
	'pass_defense_1_player_id',
	'pass_defense_1_player_name',
	'pass_defense_2_player_id',
	'pass_defense_2_player_name',
	'fumbled_1_team',
	'fumbled_1_player_id',
	'fumbled_1_player_name',
	'fumbled_2_player_id',
	'fumbled_2_player_name',
	'fumbled_2_team',
	'fumble_recovery_1_team',
	'fumble_recovery_1_yards',
	'fumble_recovery_1_player_id',
	'fumble_recovery_1_player_name',
	'fumble_recovery_2_team',
	'fumble_recovery_2_yards',
	'fumble_recovery_2_player_id',
	'fumble_recovery_2_player_name',
	'return_team',
	'return_yards',
	'replay_or_challenge',
	'replay_or_challenge_result',
	'defensive_two_point_attempt',
	'defensive_two_point_conv',
	'defensive_extra_point_attempt',
	'defensive_extra_point_conv'
]

def keys_to_text():
	file = open(r"D:\NFLDB\column_list.txt","w+")
	for key in dtypes:
		file.write("\'"+key+"\',\n")

def get_season_file(season):
	season_csv = (r"D:\NFLDB\season_stats"+str(season)+".csv")
	write_file = open(season_csv, "w+")
	return write_file

def split_db_into_seasons():
	with open(r"D:\NFLDB\nfldb.csv","r") as file:
		counter = 0
		headers = 0
		cur_season = 2009
		write_file = get_season_file(cur_season)
		db_lines = []
		for line in file:
			# get headers
			if counter == 0:
				headers = line
				write_file.write(headers)
				counter = 1
			else:
				# get season file
				cols = line.split(',')
				date_vals = cols[9].split('-')
				year = date_vals[0]
				month = date_vals[1]
				if int(year) != cur_season and int(month) > 2:
					cur_season += 1
					write_file.close()
					write_file = get_season_file(cur_season)
					write_file.write(headers)
				write_file.write(line)

def create_indexes(index,size):
	ids = []
	for i in range(size):
		ids.append(i+index)
	return ids


if __name__ == "__main__":
	# keys_to_text()
	# split_db_into_seasons()
	# mylist = []
	# for chunk in pd.read_csv(r"D:\NFLDB\season_stats2009.csv", dtype=dtypes, chunksize=20000):
	#     mylist.append(chunk)
	# big_data = pd.concat(mylist, axis= 0)
	# del mylist
	seasons = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
	# seasons = [2014,2015,2016,2017,2018]
	cur_id = 1
	for idx,season in enumerate(seasons,0):
		file = r"D:\NFLDB\season_stats"+str(season)+".csv"
		print(file)
		df = pd.read_csv(file,dtype=dtypes, usecols=cols)
		df = df[(df['play_type'].notnull()) & (df['play_type'] != 'no_play')]
		dfSize = df['play_id'].count()
		df['pid'] = create_indexes(cur_id,dfSize)
		df.set_index('pid')
		cur_id += dfSize

		action = 'replace'
		if idx > 0:
			action = 'append'
		df.to_sql('nfl_pbp', con=engine, if_exists=action,index=False)
