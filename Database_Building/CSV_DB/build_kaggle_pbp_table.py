import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:@localhost:3306/kaggle')

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
	'season', # Season
	'week', # week (1-17)
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
	'two_point_conv_result', # String indicator for result of two point conversion attempt: success, failure, safety (touchback in defensive endzone is 1 point apparently), or return.
	'td_team', # String abbreviation for which team scored the touchdown.
	'total_home_score', # Score for the home team at the start of the play.
	'total_away_score', # Score for the away team at the start of the play.
	'posteam_score', # Score the posteam at the start of the play.
	'defteam_score', # Score the defteam at the start of the play.
	'score_differential', # Score differential between the posteam and defteam at the start of the play.
	'posteam_score_post', # Score for the posteam at the end of the play.
	'defteam_score_post', # Score for the defteam at the end of the play.
	'score_differential_post', # Score differential between the posteam and defteam at the end of the play.
	'punt_blocked', # Binary indicator for if the punt was blocked.
	'incomplete_pass', # Binary indicator for if the pass was incomplete.
	'interception', # Binary indicator for if the pass was intercepted.
	'fumble_forced', # Binary indicator for if the fumble was forced.
	'fumble_not_forced', # Binary indicator for if the fumble was not forced.
	'fumble_out_of_bounds', # Binary indicator for if the fumble went out of bounds.
	'safety', # Binary indicator for whether or not a safety occurred.
	'penalty', # Binary indicator for whether or not a penalty occurred.
	'tackled_for_loss', # Binary indicator for whether or not a tackle for loss occurred.
	'fumble_lost', # Binary indicator for if the fumble was lost.
	'qb_hit', # Binary indicator if the QB was hit on the play.
	'rush_attempt', # Binary indicator for if the play was a run.
	'pass_attempt', # Binary indicator for if the play was a pass attempt (includes sacks).
	'sack', # Binary indicator for if the play ended in a sack.
	'touchdown', # Binary indicator for if the play resulted in a TD.
	'pass_touchdown', # Binary indicator for if the play resulted in a passing TD.
	'rush_touchdown', # Binary indicator for if the play resulted in a rushing TD.
	'return_touchdown', # Binary indicator for if the play resulted in a return TD.
	'extra_point_attempt', # Binary indicator for extra point attempt.
	'two_point_attempt', # Binary indicator for two point conversion attempt.
	'field_goal_attempt', # Binary indicator for field goal attempt.
	'kickoff_attempt', # Binary indicator for kickoff.
	'punt_attempt', # Binary indicator for punts.
	'fumble', # Binary indicator for if a fumble occurred.
	'complete_pass', # Binary indicator for if the pass was completed.
	'passer_player_id', # Unique identifier for the player that attempted the pass.
	'passer_player_name', # String name for the player that attempted the pass.
	'receiver_player_id', # Unique identifier for the receiver that was targeted on the pass.
	'receiver_player_name', # String name for the player that received the lateral on a reception.
	'rusher_player_id', # Unique identifier for the player that attempted the run.
	'rusher_player_name', # String name for the player that attempted the run.
	'interception_player_id', # Unique identifier for the player that intercepted the pass.
	'interception_player_name', # String name for the player that intercepted the pass.
	'punt_returner_player_id', # Unique identifier for the punt returner.
	'punt_returner_player_name', # String name for the punt returner.
	'kickoff_returner_player_name', # String name for the kickoff returner.
	'kickoff_returner_player_id',  # Unique identifier for the kickoff returner.
	'punter_player_id', # Unique identifier for the punter.
	'punter_player_name', # String name for the punter.
	'kicker_player_name', # String name for the kicker on FG or kickoff.
	'kicker_player_id', # Unique identifier for the kicker on FG or kickoff.
	'blocked_player_id', # Unique identifier for the player that blocked the punt or FG.
	'blocked_player_name', # String name for the player that blocked the punt or FG.
	'tackle_for_loss_1_player_id', # Unique identifier for one of the potential players with the tackle for loss.
	'tackle_for_loss_1_player_name', # String name for one of the potential players with the tackle for loss.
	'tackle_for_loss_2_player_id', # Unique identifier for one of the potential players with the tackle for loss.
	'tackle_for_loss_2_player_name', # String name for one of the potential players with the tackle for loss.
	'qb_hit_1_player_id', # Unique identifier for one of the potential players that hit the QB.
	'qb_hit_1_player_name', # String name for one of the potential players that hit the QB.
	'qb_hit_2_player_id', # Unique identifier for one of the potential players that hit the QB.
	'qb_hit_2_player_name', # String name for one of the potential players that hit the QB.
	'forced_fumble_player_1_team', # Team of one of the players with a forced fumble.
	'forced_fumble_player_1_player_id', # Unique identifier of one of the players with a forced fumble.
	'forced_fumble_player_1_player_name', # String name of one of the players with a forced fumble.
	'forced_fumble_player_2_team', # Team of one of the players with a forced fumble.
	'forced_fumble_player_2_player_id', # Unique identifier of one of the players with a forced fumble.
	'forced_fumble_player_2_player_name', # String name of one of the players with a forced fumble.
	'pass_defense_1_player_id', # Unique identifier of one of the players with a pass defense.
	'pass_defense_1_player_name', # String name of one of the players with a pass defense.
	'pass_defense_2_player_id', # Unique identifier of one of the players with a pass defense.
	'pass_defense_2_player_name', # String name of one of the players with a pass defense.
	'fumbled_1_team', # Team of one of the players with a fumble.
	'fumbled_1_player_id', # Unique identifier of one of the players with a fumble.
	'fumbled_1_player_name', # String name of one of the players with a fumble.
	'fumbled_2_player_id', # Unique identifier of one of the players with a fumble.
	'fumbled_2_player_name', # String name of one of the players with a fumble.
	'fumbled_2_team', # Team of one of the players with a fumble.
	'fumble_recovery_1_team', # Team of one of the players with a fumble recovery.
	'fumble_recovery_1_yards', # Yards gained by one of the players with a fumble recovery.
	'fumble_recovery_1_player_id', # Unique identifier of one of the players with a fumble recovery.
	'fumble_recovery_1_player_name', # String name of one of the players with a fumble recovery.
	'fumble_recovery_2_team', # Team of one of the players with a fumble recovery.
	'fumble_recovery_2_yards', # Yards gained by one of the players with a fumble recovery.
	'fumble_recovery_2_player_id', # Unique identifier of one of the players with a fumble recovery.
	'fumble_recovery_2_player_name', # String name of one of the players with a fumble recovery.
	'return_team', # String abbreviation of the return team.
	'return_yards', # Yards gained by the return team.
	'replay_or_challenge', # Binary indicator for whether or not a replay or challenge.
	'replay_or_challenge_result', # String indicating the result of the replay or challenge.
	'defensive_two_point_attempt', # Binary indicator whether or not the defense was able to have an attempt on a two point conversion, this results following a turnover.
	'defensive_two_point_conv', # Binary indicator whether or not the defense successfully scored on the two point conversion.
	'defensive_extra_point_attempt', # Binary indicator whether or not the defense was able to have an attempt on an extra point attempt, this results following a blocked attempt that the defense recovers the ball.
	'defensive_extra_point_conv' # Binary indicator whether or not the defense successfully scored on an extra point attempt.
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
	with open(r"D:\NFLDB\nfldb.csv","r",encoding='utf-8-sig') as file:
		counter = 0
		headers = 0
		cur_season = 2009
		cur_week = 0
		gamedate = 0
		write_file = get_season_file(cur_season)
		db_lines = []
		for line in file:
			# get headers
			if counter == 0:
				headers = ("season,"+"week,"+line)
				write_file.write(headers)
				counter = 1
			else:
				# get season
				cols = line.split(',')
				date_vals = cols[9].split('-')
				year = date_vals[0]
				month = date_vals[1]
				if int(year) != cur_season and int(month) > 2:
					cur_season += 1
					write_file.close()
					write_file = get_season_file(cur_season)
					write_file.write(headers)
					cur_week = 0
				# get week
				gameid = cols[1]
				if int(gameid) > (gamedate+600):
					cur_week += 1
					gamedate = int(gameid)
				line = (str(cur_season)+","+str(cur_week)+","+line)
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
		df.insert(0, 'pid', create_indexes(cur_id,dfSize))
		df.set_index('pid')
		cur_id += dfSize

		action = 'replace'
		if idx > 0:
			action = 'append'
		df.to_sql('nfl_pbp', con=engine, if_exists=action,index=False)
