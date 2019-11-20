import pandas as pd
import json

def get_reverse_dict(dictionary):
	return dict([[v,k] for k,v in dictionary.items()])

stat_id_map = {
	2:"punt_blocked",
	3:"first_down_rush",
	4:"first_down_pass",
	5:"first_down_penalty",
	6:"third_down_converted",
	7:"third_down_failed",
	8:"fourth_down_converted",
	9:"fourth_down_failed",
	10:"rushing_yards",
	11:"rushing_yards_td",
	12:"lateral_rushing_yards",
	13:"lateral_rushing_yards_td",
	14:"incomplete_pass",
	15:"passing_yards",
	16:"passing_yards_td",
	19:"interception",
	20:"sack_yards",
	21:"receiving_yards",
	22:"receiving_yards_td",
	23:"lateral_receiving_yards",
	24:"lateral_receiving_yards_td",
	25:"interception_return_yards",
	26:"interception_return_yards_td",
	27:"lateral_interception_return_yards",
	28:"lateral_interception_return_yards_td",
	29:"punting_yards",
	30:"punt_inside_twenty",
	31:"punt_in_endzone",
	32:"punt_touchback_kicking",
	33:"punt_return_yards",
	34:"punt_return_yards_td",
	35:"lateral_punt_return_yards",
	36:"lateral_punt_return_yards_td",
	37:"punt_out_of_bounds",
	38:"punt_downed",
	39:"punt_fair_catch",
	40:"punt_touchback_receiving",
	41:"kickoff_yards",
	42:"kickoff_inside_twenty",
	43:"kickoff_in_endzone",
	44:"kickoff_touchback_kicking",
	45:"kickoff_return_yards",
	46:"kickoff_return_yards_td",
	47:"lateral_kickoff_return_yards",
	48:"lateral_kickoff_return_yards_td",
	49:"kickoff_out_of_bounds",
	50:"kickoff_fair_catch",
	51:"kickoff_touchback_receiving",
	52:"fumble_forced",
	53:"fumble_not_forced",
	54:"fumble_out_of_bounds",
	55:"own_fumble_recovery_yards",
	56:"own_fumble_recovery_yards_td",
	57:"lateral_own_fumble_recovery_yards",
	58:"lateral_own_fumble_recovery_yards_td",
	59:"opp_fumble_recovery_yards",
	60:"opp_fumble_recovery_yards_td",
	61:"lateral_opp_fumble_recovery_yards",
	62:"lateral_opp_fumble_recovery_yards_td",
	63:"miscellaneous_yards",
	64:"miscellaneous_yards_td",
	68:"timeout",
	69:"field_goal_missed",
	70:"field_goal_made",
	71:"field_goal_blocked",
	72:"extra_point_good",
	73:"extra_point_failed",
	74:"extra_point_blocked",
	75:"two_point_rush_good",
	76:"two_point_rush_failed",
	77:"two_point_pass_good",
	78:"two_point_pass_failed",
	79:"solo_tackle",
	80:"assisted_tackle",
	82:"tackle_assist",
	83:"solo_sack_yards",
	84:"assist_sack_yards",
	85:"pass_defense_player",
	86:"punt_blocked_player",
	87:"extra_point_blocked_player",
	88:"field_goal_blocked_player",
	89:"safety",
	91:"forced_fumble_player",
	93:"penalty",
	95:"tackled_for_loss",
	96:"extra_point_safety",
	99:"two_point_rush_safety",
	100:"two_point_pass_safety",
	102:"kickoff_downed",
	103:"lateral_sack_yards",
	104:"two_point_pass_reception_good",
	105:"two_point_pass_reception_failed",
	106:"fumble_lost",
	107:"own_kickoff_recovery",
	108:"own_kickoff_recovery_td",
	110:"qb_hit",
	111:"air_yards_complete",
	112:"air_yards_incomplete",
	113:"yards_after_catch",
	115:"targeted_receiver",
	120:"tackle_for_loss_player",
	301:"extra_point_aborted",
	402:"tackle_for_loss_yards",
	410:"kickoff_yard_length",
	420:"two_point_return",
	403:"defensive_two_point_attempt",
	404:"defensive_two_point_conv",
	405:"defensive_extra_point_attempt",
	406:"defensive_extra_point_conv"
}

# binary (0,1) columns
binary_cols = [
	"punt_blocked",
	"first_down_rush",
	"first_down_pass",
	"first_down_penalty",
	"third_down_converted",
	"third_down_failed",
	"fourth_down_converted",
	"fourth_down_failed",
	"incomplete_pass",
	"interception",
	"punt_inside_twenty",
	"punt_in_endzone",
	"punt_out_of_bounds",
	"punt_downed",
	"punt_fair_catch",
	"kickoff_inside_twenty",
	"kickoff_in_endzone",
	"kickoff_out_of_bounds",
	"kickoff_fair_catch",
	"fumble_forced",
	"fumble_not_forced",
	"fumble_out_of_bounds",
	"timeout",
	"field_goal_missed",
	"field_goal_made",
	"field_goal_blocked",
	"extra_point_good",
	"extra_point_failed",
	"extra_point_blocked",
	"two_point_rush_good",
	"two_point_rush_failed",
	"two_point_pass_good",
	"two_point_pass_failed",
	"solo_tackle",
	"safety",
	"penalty",
	"tackled_for_loss",
	"extra_point_safety",
	"two_point_rush_safety",
	"two_point_pass_safety",
	"kickoff_downed",
	"two_point_pass_reception_good",
	"two_point_pass_reception_failed",
	"fumble_lost",
	"own_kickoff_recovery",
	"own_kickoff_recovery_td",
	"qb_hit",
	"extra_point_aborted",
	"two_point_return",
	"defensive_two_point_attempt",
	"defensive_two_point_conv",
	"defensive_extra_point_attempt",
	"defensive_extra_point_conv"
]
indicator_cols = {
	'rush_attempt': [
		"rushing_yards",
		"rushing_yards_td",
		"lateral_rushing_yards",
		"lateral_rushing_yards_td",
		"two_point_rush_good",
		"two_point_rush_failed",
		"two_point_rush_safety"
	],
	'pass_attempt': [
		"passing_yards",
		"passing_yards_td",
		"incomplete_pass",
		"interception",
		"sack_yards",
		"receiving_yards",
		"receiving_yards_td",
		"lateral_receiving_yards",
		"lateral_receiving_yards_td",
		"interception_return_yards",
		"interception_return_yards_td",
		"lateral_interception_return_yards",
		"lateral_interception_return_yards_td",
		"air_yards_complete",
		"air_yards_incomplete",
		"yards_after_catch",
		"targeted_receiver",
		"two_point_pass_good",
		"two_point_pass_failed",
		"two_point_pass_safety",
		"two_point_pass_reception_good",
		"two_point_pass_reception_failed"
	],
	'sack': [
		"sack_yards",
		"solo_sack_yards",
		"assist_sack_yards"
	],
	'touchdown':[
		"rushing_yards_td",
		"lateral_rushing_yards_td",
		"passing_yards_td",
		"receiving_yards_td",
		"lateral_receiving_yards_td",
		"interception_return_yards_td",
		"lateral_interception_return_yards_td",
		"kickoff_return_yards_td",
		"lateral_kickoff_return_yards_td",
		"own_fumble_recovery_yards_td",
		"lateral_own_fumble_recovery_yards_td",
		"opp_fumble_recovery_yards_td",
		"lateral_opp_fumble_recovery_yards_td",
		"miscellaneous_yards_td",
		"own_kickoff_recovery_td",
		"punt_return_yards_td",
		"lateral_punt_return_yards_td"
	],
	'pass_touchdown':[
		"passing_yards_td",
		"receiving_yards_td",
		"lateral_receiving_yards_td"
	],
	'rush_touchdown':[
		"rushing_yards_td",
		"lateral_rushing_yards_td"
	],
	'return_touchdown':[
		"interception_return_yards_td",
		"lateral_interception_return_yards_td",
		"kickoff_return_yards_td",
		"lateral_kickoff_return_yards_td",
		"punt_return_yards_td",
		"lateral_punt_return_yards_td"
	],
	'extra_point_attempt':[
		"extra_point_good",
		"extra_point_failed",
		"extra_point_blocked",
		"extra_point_safety",
		"extra_point_aborted"
	],
	'two_point_attempt':[
		"two_point_rush_good",
		"two_point_rush_failed",
		"two_point_pass_good",
		"two_point_pass_failed",
		"two_point_rush_safety",
		"two_point_pass_safety",
		"two_point_pass_reception_good",
		"two_point_pass_reception_failed",
		"two_point_return"
	],
	'field_goal_attempt':[
		"field_goal_yards_missed",
		"field_goal_yards_made",
		"field_goal_yards_blocked",
		"field_goal_blocked_player"
	],
	'kickoff_attempt':[
		"kickoff_yards",
		"kickoff_inside_twenty",
		"kickoff_in_endzone",
		"kickoff_touchback_kicking",
		"kickoff_return_yards",
		"kickoff_return_yards_td",
		"lateral_kickoff_return_yards",
		"lateral_kickoff_return_yards_td",
		"kickoff_out_of_bounds",
		"kickoff_fair_catch",
		"kickoff_touchback_receiving",
		"kickoff_downed",
		"own_kickoff_recovery",
		"own_kickoff_recovery_td",
		"kickoff_yard_length"
	],
	'punt_attempt':[
		"punt_blocked",
		"punting_yards",
		"punt_inside_twenty",
		"punt_in_endzone",
		"punt_touchback_kicking",
		"punt_return_yards",
		"punt_return_yards_td",
		"lateral_punt_return_yards",
		"lateral_punt_return_yards_td",
		"punt_out_of_bounds",
		"punt_downed",
		"punt_fair_catch",
		"punt_touchback_receiving",
		"punt_blocked_player"
	],
	'fumble':[
		"fumble_forced",
		"fumble_not_forced",
		"fumble_out_of_bounds",
		"own_fumble_recovery_yards",
		"own_fumble_recovery_yards_td",
		"lateral_own_fumble_recovery_yards",
		"lateral_own_fumble_recovery_yards_td",
		"opp_fumble_recovery_yards",
		"opp_fumble_recovery_yards_td",
		"lateral_opp_fumble_recovery_yards",
		"lateral_opp_fumble_recovery_yards_td",
		"forced_fumble_player",
		"fumble_lost"
	],
	'complete_pass':[
		"passing_yards",
		"passing_yards_td",
		"receiving_yards",
		"receiving_yards_td",
		"lateral_receiving_yards",
		"lateral_receiving_yards_td",
		"air_yards_complete",
		"yards_after_catch"
	],
	'assist_tackle':[
		"assisted_tackle",
		"tackle_assist",
		"assist_sack_yards"
	],
	'lateral_reception':[
		"lateral_receiving_yards",
		"lateral_receiving_yards_td"
	],
	'lateral_rush':[
		"lateral_rushing_yards",
		"lateral_rushing_yards_td"
	],
	'lateral_return':[
		"lateral_interception_return_yards",
		"lateral_interception_return_yards_td",
		"lateral_punt_return_yards",
		"lateral_punt_return_yards_td",
		"lateral_kickoff_return_yards",
		"lateral_kickoff_return_yards_td"
	],
	'lateral_recovery':[
		"lateral_own_fumble_recovery_yards",
		"lateral_own_fumble_recovery_yards_td",
		"lateral_opp_fumble_recovery_yards",
		"lateral_opp_fumble_recovery_yards_td"
	]
}

# player columns (player name)
passing_cols = [
	"passing_yards",
	"passing_yards_td",
	"incomplete_pass",
	"interception",
	"sack_yards",
	"air_yards_complete",
	"air_yards_incomplete",
	"two_point_pass_good",
	"two_point_pass_failed",
	"two_point_pass_safety"
]

# process stat id
def process_statid(stat_id):
	column = stat_id_map[stat_id]

	# process binary columns
	if(column in binary_cols):
		df.at[0,column] = 1
	else:
		df.at[0,column] = 0
	for key in indicator_cols:
		if(column in indicator_cols[key]):
			df.at[0,key] = 1
		else:
			df.at[0,key] = 0



mystr = open("json_test.txt","r").read()

y = json.loads(mystr)