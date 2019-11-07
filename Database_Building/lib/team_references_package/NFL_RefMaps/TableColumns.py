class TableColumns:
	def __init__(self):
		self.football_ref = {
		    'all_player_offense':[
				'gameid',
				'playerid',
				'player',
				'team',
				'pass_cmp',
				'pass_att',
				'pass_yds',
				'pass_td',
				'int',
				'sack',
				'sack_yds',
				'lng',
				'rate',
				'rush_att',
				'rush_yds',
				'rush_tds',
				'rush_lng',
				'rec_tgts',
				'rec',
				'rec_yds',
				'rec_tds',
				'rec_lng',
				'fmb',
				'fl'
		    ],
		    'all_targets_directions':[
				'gameid',
				'playerid',
			    'player',
				'team',
				'sl_tgt',
				'sl_rec',
				'sl_yds',
				'sl_tds',
				'sm_tgt',
				'sm_rec',
				'sm_yds',
				'sm_tds',
				'sr_tgt',
				'sr_rec',
				'sr_yds',
				'sr_tds',
				'dl_tgt',
				'dl_rec',
				'dl_yds',
				'dl_tds',
				'dm_tgt',
				'dm_rec',
				'dm_yds',
				'dm_tds',
				'dmr_tgt',
				'dmr_rec',
				'dmr_yds',
				'dmr_tds'
		    ],
		    'all_rush_directions':[
				'gameid',
				'playerid',
			    'player',
				'team',
				'le_att',
				'le_yds',
				'le_td',
				'lt_att',
				'lt_yds',
				'lt_td',
				'lg_att',
				'lg_yds',
				'lg_td',
				'm_att',
				'm_yds',
				'm_td',
				're_att',
				're_yds',
				're_td',
				'rt_att',
				'rt_yds',
				'rt_td',
				'rg_att',
				'rg_yds',
				'rg_td',
		    ],
		    'all_player_defense':[
				'gameid',
				'playerid',
		        'player',
				'team',
				'int',
				'int_yards',
				'int_td',
				'int_lng',
				'pd',
				'sacks',
				'tckl_comb',
				'tckl_solo',
				'tckl_ast',
				'tckl_for_loss',
				'qbhits',
				'fr',
				'fr_yds',
				'fr_tds',
				'ff'
		    ],
		    'all_returns':[
				'gameid',
				'playerid',
				'player',
				'team',
				'kor',
				'ko_yds',
				'ko_ypr',
				'ko_td',
				'ko_lng',
				'pr',
				'pr_yds',
				'pr_ypr',
				'pr_tds',
				'pr_lng'
		    ],
		    'all_home_snap_counts':[
				'gameid',
				'playerid',
				'player',
				'pos',
				'off_snaps',
				'off_pct',
				'def_snaps',
				'def_pct',
				'st_snaps',
				'st_pct'
		    ],
		    'all_vis_snap_counts':[
				'gameid',
				'playerid',
				'player',
				'pos',
				'off_snaps',
				'off_pct',
				'def_snaps',
				'def_pct',
				'st_snaps',
				'st_pct'
		    ]
		}
		self.fantasy_pros = {
			'qb_projections':[
				'pid',
				'name',
				'team',
				'week',
				'pass_att',
				'pass_comp',
				'pass_yards',
				'pass_tds',
				'int',
				'rush_att',
				'rush_yds',
				'rush_tds',
				'fl',
				'fantasy_points'
			],
			'rb_projections':[
				'pid',
				'name',
				'team',
				'week',
				'rush_att',
				'rush_yds',
				'rush_tds',
				'rec',
				'rec_yds',
				'rec_tds',
				'fl',
				'fantasy_points'
			],
			'wr_projections':[
				'pid',
				'name',
				'team',
				'week',
				'rec',
				'rec_yds',
				'rec_tds',
				'rush_att',
				'rush_yds',
				'rush_tds',
				'fl',
				'fantasy_points'
			],
			'te_projections':[
				'pid',
				'name',
				'team',
				'week',
				'rec',
				'rec_yds',
				'rec_tds',
				'fl',
				'fantasy_points'
			],
			'dst_projections':[
				'pid',
				'name',
				'team',
				'week',
				'sack',
				'int',
				'fr',
				'ff',
				'td',
				'safety',
				'pa',
				'yds_agn',
				'fantasy_points'
			],
			'k_projections':[
				'pid',
				'name',
				'team',
				'week',
				'fg',
				'fga',
				'xpt',
				'fantasy_points'
			],
			'rankings':[
				'pid',
				'name',
				'team',
				'opp',
				'home_away',
				'best',
				'worst',
				'avg',
				'std_dev',
				'proj_points'
			]

		}
		self.nflapi = {
			'pbp_cols':[
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
				'time_half', # Time remaining in the half
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
				'qb_kneel', # Binary indicator for whether or not the QB kneeled.
				'qb_spike', # Binary indicator for whether or not the QB spiked the ball.
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
				'sack_player_id',
				'sack_player_name',
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
				'receiver_player_name', # String name for the player that received the reception.
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
		}
