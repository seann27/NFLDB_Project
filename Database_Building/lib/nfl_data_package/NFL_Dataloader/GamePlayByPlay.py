#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import urllib
import json
import math
import re
from NFL_RefMaps import TableColumns

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

# returns home_team, away_team abbreviations
def get_teams(jstr):
    game_id = next(iter(jstr))
    return jstr[game_id]['home']['abbr'],jstr[game_id]['away']['abbr']

# returns game date formatted MM-DD-YYYY
def get_date(jstr):
    gameid = next(iter(jstr))
    return gameid[4:6]+"-"+gameid[6:8]+"-"+gameid[0:4]

# returns array of drive ids
def get_drive_ids(jstr):
    gameid = next(iter(jstr))
    drive_ids = []
    for drive in jstr[gameid]['drives']:
        drive_ids.append(drive)
    return drive_ids[:-1]

# returns dictionary of plays for a specific drive
def get_plays(drive,jstr):
    gameid = next(iter(jstr))
    return jstr[gameid]['drives'][drive]['plays']

# returns quarter_end indicator, time left in half
def get_time_status(qtr,time):
    ts = {}
    time = time.split(':')
    qtr = (int(qtr)%2)*15
    ts['qtr_end'] = 0
    ts['time_left'] = 0
    if(len(time)<2):
        ts['qtr_end'] = 1
        ts['time_left'] = 0
    else:
        seconds_remaining = float(int(time[1])/60)
        minutes_remaining = int(time[0])+qtr
        ts['time_left'] = minutes_remaining+seconds_remaining
    return ts

def get_yardline_100(yrdline,posteam):
    if(yrdline == ''):
        return(0)
    elif(yrdline == '50'):
        return yrdline
    else:
        territory,location = yrdline.split()
        if(territory == posteam):
            location = 100-int(location)
        return int(location)

def get_yards_gained(players):
    yards_gained_cols = [
        "rushing_yards",
        "rushing_yards_td",
        "lateral_rushing_yards",
        "lateral_rushing_yards_td",
        "passing_yards",
        "passing_yards_td",
        "sack_yards",
        "receiving_yards",
        "receiving_yards_td",
        "lateral_receiving_yards",
        "lateral_receiving_yards_td"
    ]
    yards_gained = 0
    for player in players:
        for seq in players[player]:
            statId = seq['statId']
            if(stat_id_map[statId] in yards_gained_cols):
                yards_gained = float(seq['yards'])

    return yards_gained

def get_qb_action(desc):
    qba = {}
    desc = desc.lower()
    qba['qb_kneel'] = 0
    qba['qb_spike'] = 0
    qba['qb_scramble'] = 0
    qba['shotgun'] = 0
    qba['no_huddle'] = 0
    if(desc.find(' kneels ') > -1):
        qba['qb_kneel'] = 1
    if(desc.find(' spiked ') > -1):
        qba['qb_spike'] = 1
    if(desc.find(' scrambles ') > -1):
        qba['qb_scramble'] = 1
    if(desc.find('shotgun') > -1):
        qba['shotgun'] = 1
    if(desc.find('no huddle') > -1):
        qba['no_huddle'] = 1

    return qba

def get_penalties(players):
    p = {}
    p['penalty_yards'] = 0
    p['penalty_team'] = 'N/A'
    p['penalty_player_id'] = 'N/A'
    p['penalty_player_name'] = 'N/A'
    for player in players:
        for seq in players[player]:
            statId = seq['statId']
            if(stat_id_map[statId] == 'penalty'):
                p['penalty_team'] = seq['clubcode']
                p['penalty_player_id'] = player
                p['penalty_player_name'] = seq['playerName']
                p['penalty_yards'] = float(seq['yards'])
    return p

def get_sack(players):
    s = {}
    cols = [
        "sack_yards",
        "solo_sack_yards",
        "assist_sack_yards"
    ]
    s['sack'] = 0
    s['sack_pid'] = 'N/A'
    s['sack_name'] = 'N/A'
    for player in players:
        for seq in players[player]:
            statId = seq['statId']
            if(stat_id_map[statId] in cols):
                s['sack'] = 1
                s['sack_pid'] = player
                s['sack_name'] = seq['playerName']
    return s

def get_touchdowns(players):
    tds = {}
    misc_td_cols = [
        "own_fumble_recovery_yards_td",
        "lateral_own_fumble_recovery_yards_td",
        "opp_fumble_recovery_yards_td",
        "lateral_opp_fumble_recovery_yards_td",
        "miscellaneous_yards_td",
        "own_kickoff_recovery_td",
    ]
    pass_td_cols = [
        "passing_yards_td",
        "receiving_yards_td",
        "lateral_receiving_yards_td"
    ]
    rush_td_cols = [
        "rushing_yards_td",
        "lateral_rushing_yards_td"
    ]
    return_td_cols = [
        "interception_return_yards_td",
        "lateral_interception_return_yards_td",
        "kickoff_return_yards_td",
        "lateral_kickoff_return_yards_td",
        "punt_return_yards_td",
        "lateral_punt_return_yards_td"
    ]
    tds['touchdown'] = 0
    tds['pass_touchdown'] = 0
    tds['rush_touchdown'] = 0
    tds['return_touchdown'] = 0
    tds['td_team'] = 'N/A'
    for player in players:
        for seq in players[player]:
            statId = seq['statId']
            if(stat_id_map[statId] in pass_td_cols):
                tds['pass_touchdown'] = 1
                tds['touchdown'] = 1
                tds['td_team'] = seq['clubcode']
            if(stat_id_map[statId] in rush_td_cols):
                tds['rush_touchdown'] = 1
                tds['touchdown'] = 1
                tds['td_team'] = seq['clubcode']
            if(stat_id_map[statId] in return_td_cols):
                tds['return_touchdown'] = 1
                tds['touchdown'] = 1
                tds['td_team'] = seq['clubcode']
            if(stat_id_map[statId] in misc_td_cols):
                tds['touchdown'] = 1
                tds['td_team'] = seq['clubcode']
    return tds

def get_special_teams(mpd,idx,players):
    xp_att_cols = [
        "extra_point_good",
        "extra_point_failed",
        "extra_point_blocked",
        "extra_point_safety",
        "extra_point_aborted"
    ]
    twopt_att_cols = [
        "two_point_rush_good",
        "two_point_rush_failed",
        "two_point_pass_good",
        "two_point_pass_failed",
        "two_point_rush_safety",
        "two_point_pass_safety",
        "two_point_pass_reception_good",
        "two_point_pass_reception_failed",
        "two_point_return"
    ]
    fg_att_cols = [
        "field_goal_missed",
        "field_goal_made",
        "field_goal_blocked",
        "field_goal_blocked_player"
    ]
    kickoff_att_cols = [
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
    ]
    punt_att_cols = [
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
    ]
    indicators = [
        "defensive_extra_point_attempt",
        "defensive_extra_point_conv",
        "defensive_two_point_attempt",
        "defensive_two_point_conv",
    ]
    kicker_cols = [
        "kickoff_yards",
        "kickoff_inside_twenty",
        "kickoff_in_endzone",
        "kickoff_touchback_kicking",
        "kickoff_out_of_bounds",
        "field_goal_yards_missed",
        "field_goal_yards_made",
        "field_goal_yards_blocked",
        "extra_point_good",
        "extra_point_failed",
        "extra_point_blocked",
        "kickoff_yard_length"
    ]
    kickoff_returner_cols = [
        "kickoff_return_yards",
        "kickoff_return_yards_td",
        "kickoff_fair_catch"
    ]
    punter_player_cols = [
        "punting_yards",
        "punt_inside_twenty",
        "punt_in_endzone",
        "punt_touchback_kicking",
        "punt_out_of_bounds"
    ]
    punt_returner_cols = [
        "punt_return_yards",
        "punt_return_yards_td",
        "punt_fair_catch"
    ]
    blocked_player_cols = [
        "punt_blocked_player",
        "extra_point_blocked_player",
        "field_goal_blocked_player"
    ]
    player_cols = {
        'kicker' : kicker_cols,
        'kickoff_returner' : kickoff_returner_cols,
        'punter' : punter_player_cols,
        'punt_returner' : punt_returner_cols,
        'blocked' : blocked_player_cols
    }
    st = {
        'xp_att' : 0,
        'kick_distance' : 0,
        'extra_point_result' : 'N/A',
        'defensive_extra_point_attempt' : 0,
        'defensive_extra_point_conv' : 0,
        'twopt_att' : 0,
        'two_point_conv_result' : 'N/A',
        'two_point_yds_gained' : 0,
        'defensive_two_point_attempt' : 0,
        'defensive_two_point_conv' : 0,
        'fg_att' : 0,
        'field_goal_result' : 'N/A',
        'kickoff_att' : 0,
        'kicker_player_name' : 'N/A',
        'kicker_player_id' : 'N/A',
        'kickoff_returner_player_name' : 'N/A',
        'kickoff_returner_player_id' : 'N/A',
        'punt_att' : 0,
        'punter_player_id' : 'N/A',
        'punter_player_name' : 'N/A',
        'punt_returner_player_id' : 'N/A',
        'punt_returner_player_name' : 'N/A',
        'blocked_player_id' : 'N/A',
        'blocked_player_name' : 'N/A',
        'sp_team' : 'N/A',
        'points_scored' : 0,
    }

    for player in players:
        for seq in players[player]:
            stat = stat_id_map[seq['statId']]
            if stat in xp_att_cols:
                st['xp_att'] = 1
                st['kick_distance'] = mpd['yardline_100'][idx]+18
                if stat == 'extra_point_good':
                    st['extra_point_result'] = 'made'
                    st['sp_team'] = seq['clubcode']
                    st['points_scored'] = 1
                if stat == 'extra_point_missed':
                    st['extra_point_result'] = 'failed'
                if stat == 'extra_point_blocked':
                    st['extra_point_result'] = 'blocked'
                if stat == 'extra_point_safety':
                    st['extra_point_result'] = 'safety'
                    st['sp_team'] = seq['clubcode']
                    st['points_scored'] = 1
                if stat == 'extra_point_aborted':
                    st['extra_point_result'] = 'aborted'
            if stat in twopt_att_cols:
                st['twopt_att'] = 1
                good = [
                    "two_point_rush_good",
                    "two_point_pass_good",
                    "two_point_pass_reception_good",
                ]
                failed = [
                    "two_point_rush_failed",
                    "two_point_pass_failed",
                    "two_point_pass_reception_failed",
                ]
                safety = [
                    "two_point_rush_safety",
                    "two_point_pass_safety",
                ]
                if stat in good:
                    st['two_point_conv_result'] = 'success'
                    st['two_point_yds_gained'] = seq['yards']
                    st['sp_team'] = seq['clubcode']
                    st['points_scored'] = 2
                if stat in failed:
                    st['two_point_conv_result'] = 'failure'
                if stat in safety:
                    st['two_point_conv_result'] = 'safety'
                    st['sp_team'] = seq['clubcode']
                    st['points_scored'] = 2
                if stat == "two_point_return":
                    st['two_point_conv_result'] = 'return'
            if stat in fg_att_cols:
                st['fg_att'] = 1
                st['kick_distance'] = mpd['yardline_100'][idx]+18
                if stat == 'field_goal_made':
                    st['field_goal_result'] = 'made'
                    st['sp_team'] = seq['clubcode']
                    st['points_scored'] = 3
                if stat == 'field_goal_missed':
                    st['field_goal_result'] = 'missed'
                if stat == 'field_goal_blocked':
                    st['field_goal_result'] = 'blocked'
            if stat in kickoff_att_cols:
                st['kickoff_att'] = 1
            if stat in punt_att_cols:
                st['punt_att'] = 1
            if stat in indicators:
                st[stat] = 1
            for key,val in player_cols.items():
                if stat in val:
                    st[key+'_player_id'] = player
                    st[key+'_player_name'] = seq['playerName']

    return st

def get_turnovers(players):
    to = {}
    fum_cols = [
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
    ]
    indicator_cols = [
        "fumble_forced",
        "fumble_not_forced",
        "fumble_out_of_bounds",
        "fumble_lost",
        "interception"
    ]
    int_player_cols = [
        "interception_return_yards",
        "interception_return_yards_td"
    ]
    forced_fumble_player_cols = [
        "forced_fumble_player"
    ]
    fumbled_player_cols = [
        "fumble_forced",
        "fumble_not_forced",
        "fumble_out_of_bounds",
        "fumble_lost"
    ]
    fumble_recovery_player_cols = [
        "own_fumble_recovery_yards",
        "own_fumble_recovery_yards_td",
        "opp_fumble_recovery_yards",
        "opp_fumble_recovery_yards_td"
    ]

    player_cols = {
        'interception':int_player_cols,
        'forced_fumble_player':forced_fumble_player_cols,
        'fumble':fumbled_player_cols,
        'fumble_recovery':fumble_recovery_player_cols
    }
    tracker = {
        'interception':1,
        'forced_fumble_player':1,
        'fumble':1,
        'fumble_recovery':1
    }
    to = {
        'fumble' : 0,
        'fumble_forced' : 0,
        'fumble_not_forced' : 0,
        'fumble_out_of_bounds' : 0,
        'fumble_lost' : 0,
        'interception' : 0,
        'interception_player_id' : 'N/A',
        'interception_player_name' : 'N/A',
        'forced_fumble_player_1_team' : 'N/A',
        'forced_fumble_player_1_player_id' : 'N/A',
        'forced_fumble_player_1_player_name' : 'N/A',
        'forced_fumble_player_2_team' : 'N/A',
        'forced_fumble_player_2_player_id' : 'N/A',
        'forced_fumble_player_2_player_name' : 'N/A',
        'fumbled_1_team' : 'N/A',
        'fumbled_1_player_id' : 'N/A',
        'fumbled_1_player_name' : 'N/A',
        'fumbled_2_player_id' : 'N/A',
        'fumbled_2_player_name' : 'N/A',
        'fumbled_2_team' : 'N/A',
        'fumble_recovery_1_team' : 'N/A',
        'fumble_recovery_1_yards' : 0,
        'fumble_recovery_1_player_id' : 'N/A',
        'fumble_recovery_1_player_name' : 'N/A',
        'fumble_recovery_2_team' : 'N/A',
        'fumble_recovery_2_yards' : 0,
        'fumble_recovery_2_player_id' : 'N/A',
        'fumble_recovery_2_player_name' : 'N/A'
    }
    for player in players:
        for seq in players[player]:
            stat = stat_id_map[seq['statId']]
            if(stat in fum_cols):
                to['fumble'] = 1
            if stat in indicator_cols:
                to[stat] = 1
            for key,val in player_cols.items():
                if stat in val:
                    plyr = str(tracker[key])
                    if key != 'interception':
                        to[key+"_"+plyr+"_player_id"] = player
                        to[key+"_"+plyr+"_player_name"] = seq['playerName']
                        to[key+"_"+plyr+"_team"] = seq['clubcode']
                        if key == 'fumble_recovery':
                            to[key+"_"+plyr+"_yards"] = seq['yards']
                        tracker[key] += 1
                    else:
                        to[key+"_player_id"] = player
                        to[key+"_player_name"] = seq['playerName']


    return to

def get_pass_info(players,desc):
    pass_att_cols = [
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
    ]
    completed_pass_cols = [
        "passing_yards",
        "passing_yards_td",
        "receiving_yards",
        "receiving_yards_td",
        "lateral_receiving_yards",
        "lateral_receiving_yards_td",
        "air_yards_complete",
        "yards_after_catch"
    ]
    passer_cols = [
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
    receiver_cols = [
        "receiving_yards",
        "receiving_yards_td",
        "yards_after_catch",
        "targeted_receiver",
        "two_point_pass_reception_good",
        "two_point_pass_reception_failed",
        "lateral_receiving_yards",
        "lateral_receiving_yards_td"
    ]
    off = {}
    off['pass_att'] = 0
    off['complete_pass'] = 0
    off['incomplete_pass'] = 0
    off['passer_pid'] = 'N/A'
    off['passer_name'] = 'N/A'
    off['receiver_pid'] = 'N/A'
    off['receiver_name'] = 'N/A'
    off['pass_length'] = 'N/A'
    off['pass_location'] = 'N/A'
    off['air_yards'] = 0
    off['yards_after_catch'] = 0

    for player in players:
        for seq in players[player]:
            stat = stat_id_map[seq['statId']]
            if stat in pass_att_cols:
                off['pass_att'] = 1
                if stat == 'air_yards_complete' or stat == 'air_yards_incomplete':
                    off['air_yards'] = seq['yards']
                if stat == 'yards_after_catch':
                    off['yards_after_catch'] = seq['yards']
            if stat == 'incomplete_pass':
                off['incomplete_pass'] = 1
            elif stat in completed_pass_cols:
                off['complete_pass'] = 1
            if stat in passer_cols:
                off['passer_pid'] = player
                off['passer_name'] = seq['playerName']
            if stat in receiver_cols:
                off['receiver_pid'] = player
                off['receiver_name'] = seq['playerName']

    # get pass length, location
    ple = re.search('(short|deep)',desc)
    plo = re.search('(left|middle|right)',desc)
    if ple:
        off['pass_length'] = ple.group(0)
    if plo and off['pass_att'] == 1:
        off['pass_location'] = plo.group(0)

    return off

def get_rush_info(players,desc):
    r = {}
    rush_cols = [
        "rushing_yards",
        "rushing_yards_td",
        "two_point_rush_good",
        "two_point_rush_failed",
        "two_point_rush_safety",
        "lateral_rushing_yards",
        "lateral_rushing_yards_td"
    ]
    r['rush_att'] = 0
    r['rusher_pid'] = 'N/A'
    r['rusher_name'] = 'N/A'
    r['run_location'] = 'N/A'
    r['run_gap'] = 'N/A'

    for player in players:
        for seq in players[player]:
            statId = seq['statId']
            if(stat_id_map[statId] in rush_cols):
                r['rush_att'] = 1
                r['rusher_pid'] = player
                r['rusher_name'] = seq['playerName']

    # get pass length, location
    rgap = re.search('(end|guard|tackle) (?!zone)',desc)
    rloc = re.search('(left|middle|right)',desc)
    if rgap:
        r['run_gap'] = rgap.group(0)
    if rloc and r['rush_att'] == 1:
        r['run_location'] = rloc.group(0)

    return r

def get_defensive_stats(players):
    indicators = [
        'safety',
        'tackled_for_loss',
        'qb_hit'
    ]
    return_cols = [
        "punt_touchback_receiving",
        "punt_downed","punt_fair_catch",
        "kickoff_fair_catch",
        "kickoff_touchback_receiving"
    ]
    defense = {
        'safety' : 0,
        'tackled_for_loss' : 0,
        'qb_hit' : 0,
        'tackle_for_loss_1_player_id' : 'N/A',
        'tackle_for_loss_1_player_name' : 'N/A',
        'tackle_for_loss_2_player_id' : 'N/A',
        'tackle_for_loss_2_player_name' : 'N/A',
        'qb_hit_1_player_id' : 'N/A',
        'qb_hit_1_player_name' : 'N/A',
        'qb_hit_2_player_id' : 'N/A',
        'qb_hit_2_player_name' : 'N/A',
        'pass_defense_1_player_id' : 'N/A',
        'pass_defense_1_player_name' : 'N/A',
        'pass_defense_2_player_id' : 'N/A',
        'pass_defense_2_player_name' : 'N/A',
        'return_team': 'N/A',
        'return_yards': 0
    }
    tfl = 1
    qbh = 1
    pdp = 1
    for player in players:
        for seq in players[player]:
            stat = stat_id_map[seq['statId']]
            if stat in indicators:
                defense[stat] = 1
            if stat in return_cols:
                defense['return_team'] = seq['clubcode']
                defense['return_yards'] = seq['yards']
            if stat == 'tackle_for_loss':
                pid_key = 'tackle_for_loss_'+str(tfl)+'_player_id'
                pid_name = 'tackle_for_loss_'+str(tfl)+'_player_name'
                defense[pid_key] = player
                defense[pid_name] = seq['playerName']
                tfl += 1
            if stat == 'qb_hit':
                pid_key = 'qb_hit_'+str(qbh)+'_player_id'
                pid_name = 'qb_hit_'+str(qbh)+'_player_name'
                defense[pid_key] = player
                defense[pid_name] = seq['playerName']
                qbh += 1
            if stat == 'pass_defense_player':
                pid_key = 'pass_defense_'+str(pdp)+'_player_id'
                pid_name = 'pass_defense_'+str(pdp)+'_player_name'
                defense[pid_key] = player
                defense[pid_name] = seq['playerName']
                pdp += 1
    return defense

def get_play_type(mpd,idx):

    # if penalty, make sure play is valid
    if (mpd['pass_attempt'][idx] == 1):
        play_type = 'pass'
    elif (mpd['rush_attempt'][idx] == 1):
        play_type = 'run'
    elif (mpd['punt_attempt'][idx] == 1):
        play_type = 'punt'
    elif (mpd['kickoff_attempt'][idx] == 1):
        play_type = 'kickoff'
    elif (mpd['qb_spike'][idx] == 1):
        play_type = 'qb_spike'
    elif (mpd['qb_kneel'][idx] == 1):
        play_type = 'qb_kneel'
    elif (mpd['field_goal_attempt'][idx] == 1):
        play_type = 'field goal'
    elif (mpd['extra_point_attempt'][idx] == 1):
        play_type = 'extra point'
    else:
        play_type = 'No Play'

    return play_type

def get_points_scored(ps):
    ti = 1
    home_team_score = ps['home_team_score']
    away_team_score = ps['away_team_score']
    if ps['posteam'] == ps['home_team']:
        posteam_score = home_team_score
        defteam_score = away_team_score
    elif ps['posteam'] == ps['away_team']:
        posteam_score = away_team_score
        defteam_score = home_team_score
        ti = 0
    else:
        ti = -1

    if ti >= 0:
        score_differential = posteam_score - defteam_score
        posteam_score_post = posteam_score
        defteam_score_post = defteam_score
        if ps['sp'] > 0:
            if ps['points_scored_team'] == ps['posteam']:
                posteam_score_post += ps['points_scored']
            else:
                defteam_score_post += ps['points_scored']
        score_differential_post = posteam_score_post - defteam_score_post
    else:
        posteam_score = 'N/A'
        defteam_score = 'N/A'
        score_differential = 'N/A'
        posteam_score_post = 'N/A'
        defteam_score_post = 'N/A'
        score_differential_post = 'N/A'

    if ti == 1:
        home_team_score_post = posteam_score_post
        away_team_score_post = defteam_score_post
    elif ti == 0:
        home_team_score_post = defteam_score_post
        away_team_score_post = posteam_score_post
    else:
        home_team_score_post = home_team_score
        away_team_score_post = away_team_score

    psn = {
        'home_team_score' : home_team_score,
        'away_team_score' : away_team_score,
        'home_team_score_post' : home_team_score_post,
        'away_team_score_post' : away_team_score_post,
        'posteam_score' : posteam_score,
        'defteam_score' : defteam_score,
        'score_differential' : score_differential,
        'posteam_score_post' : posteam_score_post,
        'defteam_score_post' : defteam_score_post,
        'score_differential_post' : score_differential_post
    }

    return psn

# returns dictionary with empty columns
# static attributes (like game date) are stored as values, everything else stored as arrays
def init_df():
    mpd = {}

    # static cols
    mpd['game_id'] = ''
    mpd['home_team'] = ''
    mpd['away_team'] = ''

    # non-static cols
    mpd['play_id'] = []
    mpd['drive'] = []
    mpd['posteam'] = []
    mpd['sp'] = []
    mpd['notes'] = []
    mpd['qtr'] = []
    mpd['down'] = []
    mpd['quarter_end'] = []
    mpd['time_half'] = []
    mpd['time'] = []
    mpd['ydstogo'] = []
    mpd['ydsnet'] = []
    mpd['desc'] = []
    mpd['yardline_100'] = []
    mpd['yards_gained'] = []
    mpd['shotgun'] = []
    mpd['no_huddle'] = []
    mpd['play_type'] = []
    mpd['replay_or_challenge'] = []
    mpd['replay_or_challenge_result'] = []

    # penalties
    mpd['penalty_yards'] = []
    mpd['penalty_team'] = []
    mpd['penalty_player_id'] = []
    mpd['penalty_player_name'] = []

    # sacks
    mpd['sack'] = []
    mpd['sack_player_id'] = []
    mpd['sack_player_name'] = []

    # touchdowns
    mpd['touchdown'] = []
    mpd['pass_touchdown'] = []
    mpd['rush_touchdown'] = []
    mpd['return_touchdown'] = []
    mpd['td_team'] = []

    # special teams
    mpd['extra_point_attempt'] = []
    mpd['two_point_attempt'] = []
    mpd['field_goal_attempt'] = []
    mpd['kickoff_attempt'] = []
    mpd['punt_attempt'] = []
    mpd['field_goal_result'] = []
    mpd['kick_distance'] = []
    mpd['extra_point_result'] = []
    mpd['two_point_conv_result'] = []
    mpd['punt_returner_player_id'] = []
    mpd['punt_returner_player_name'] = []
    mpd['kickoff_returner_player_name'] = []
    mpd['kickoff_returner_player_id'] = []
    mpd['punter_player_id'] = []
    mpd['punter_player_name'] = []
    mpd['kicker_player_name'] = []
    mpd['kicker_player_id'] = []
    mpd['blocked_player_id'] = []
    mpd['blocked_player_name'] = []
    mpd['defensive_two_point_attempt'] = []
    mpd['defensive_two_point_conv'] = []
    mpd['defensive_extra_point_attempt'] = []
    mpd['defensive_extra_point_conv'] = []

    # turnovers
    mpd['fumble'] = []
    mpd['fumble_forced'] = []
    mpd['fumble_not_forced'] = []
    mpd['fumble_out_of_bounds'] = []
    mpd['fumble_lost'] = []
    mpd['interception'] = []
    mpd['interception_player_id'] = []
    mpd['interception_player_name'] = []
    mpd['forced_fumble_player_1_team'] = []
    mpd['forced_fumble_player_1_player_id'] = []
    mpd['forced_fumble_player_1_player_name'] = []
    mpd['forced_fumble_player_2_team'] = []
    mpd['forced_fumble_player_2_player_id'] = []
    mpd['forced_fumble_player_2_player_name'] = []
    mpd['fumbled_1_team'] = []
    mpd['fumbled_1_player_id'] = []
    mpd['fumbled_1_player_name'] = []
    mpd['fumbled_2_player_id'] = []
    mpd['fumbled_2_player_name'] = []
    mpd['fumbled_2_team'] = []
    mpd['fumble_recovery_1_team'] = []
    mpd['fumble_recovery_1_yards'] = []
    mpd['fumble_recovery_1_player_id'] = []
    mpd['fumble_recovery_1_player_name'] = []
    mpd['fumble_recovery_2_team'] = []
    mpd['fumble_recovery_2_yards'] = []
    mpd['fumble_recovery_2_player_id'] = []
    mpd['fumble_recovery_2_player_name'] = []

    # pass info
    mpd['pass_attempt'] = []
    mpd['complete_pass'] = []
    mpd['incomplete_pass'] = []
    mpd['passer_player_id'] = []
    mpd['passer_player_name'] = []
    mpd['receiver_player_id'] = []
    mpd['receiver_player_name'] = []
    mpd['pass_length'] = []
    mpd['pass_location'] = []
    mpd['air_yards'] = []
    mpd['yards_after_catch'] = []

    # rush info
    mpd['rush_attempt'] = []
    mpd['rusher_player_id'] = []
    mpd['rusher_player_name'] = []
    mpd['run_location'] = []
    mpd['run_gap'] = []

    # qb action
    mpd['qb_scramble'] = []
    mpd['qb_kneel'] = []
    mpd['qb_spike'] = []
    mpd['qb_dropback'] = []

    # points scored
    mpd['total_home_score'] = []
    mpd['total_away_score'] = []
    mpd['posteam_score'] = []
    mpd['defteam_score'] = []
    mpd['score_differential'] = []
    mpd['posteam_score_post'] = []
    mpd['defteam_score_post'] = []
    mpd['score_differential_post'] = []

    # defensive stats
    mpd['safety'] = []
    mpd['tackled_for_loss'] = []
    mpd['qb_hit'] = []
    mpd['tackle_for_loss_1_player_id'] = []
    mpd['tackle_for_loss_1_player_name'] = []
    mpd['tackle_for_loss_2_player_id'] = []
    mpd['tackle_for_loss_2_player_name'] = []
    mpd['qb_hit_1_player_id'] = []
    mpd['qb_hit_1_player_name'] = []
    mpd['qb_hit_2_player_id'] = []
    mpd['qb_hit_2_player_name'] = []
    mpd['pass_defense_1_player_id'] = []
    mpd['pass_defense_1_player_name'] = []
    mpd['pass_defense_2_player_id'] = []
    mpd['pass_defense_2_player_name'] = []
    mpd['return_team'] = []
    mpd['return_yards'] = []

    return mpd

class NFLAPI_Processor:

	def __init__(self,gameid):
		self.gameid = gameid
		link = "http://www.nfl.com/liveupdate/game-center/"+str(gameid)+'/'+str(gameid)+"_gtd.json"
		with urllib.request.urlopen(link) as url:
		    self.nflapi = json.loads(url.read().decode())
		self.mpd = init_df()

	def api_to_excel(self):
		excel_file = str(gameid)+"pbptable.xls"
		self.mpd.to_excel(excel_file)

	def process_nflapi(self):
		test_sp = []
		test_notes = []
		self.mpd['game_id'] = self.gameid
		self.mpd['home_team'],self.mpd['away_team'] = get_teams(self.nflapi)
		self.mpd['date'] = get_date(self.nflapi)
		drives = get_drive_ids(self.nflapi)
		idx = 0
		home_team_score = 0
		away_team_score = 0
		for drive in drives:
		    plays = get_plays(drive,self.nflapi)
		    for play in plays:
		        # get play summary
		        self.mpd['drive'].append(drive)
		        self.mpd['play_id'].append(play)
		        details = plays[play]
		        self.mpd['sp'].append(details['sp'])
		        points_scored = 0
		        points_scored_team = 'N/A'
		        self.mpd['notes'].append(details['note'])
		        self.mpd['qtr'].append(details['qtr'])
		        self.mpd['down'].append(details['down'])
		        self.mpd['time'].append(details['time'])
		        ts = get_time_status(details['qtr'],details['time'])
		        self.mpd['quarter_end'].append(ts['qtr_end'])
		        self.mpd['time_half'].append(ts['time_left'])
		        self.mpd['ydstogo'].append(details['ydstogo'])
		        self.mpd['ydsnet'].append(details['ydsnet'])
		        self.mpd['desc'].append(details['desc'])
		        self.mpd['posteam'].append(details['posteam'])
		        self.mpd['yardline_100'].append(get_yardline_100(details['yrdln'],details['posteam']))
		        desc = details['desc']
		        roc = re.search('(Replay Official reviewed)|( challenge(d)? )',desc)
		        if roc:
		            self.mpd['replay_or_challenge'].append(1)
		            desc = desc.lower()
		            result = re.search('(upheld|reversed|confirmed)',desc)
		            self.mpd['replay_or_challenge_result'].append(result.group(0))
		        else:
		            self.mpd['replay_or_challenge'].append(0)
		            self.mpd['replay_or_challenge_result'].append('N/A')

		        # get penalty info
		        p = get_penalties(details['players'])
		        self.mpd['penalty_yards'].append(p['penalty_yards'])
		        self.mpd['penalty_team'].append(p['penalty_team'])
		        self.mpd['penalty_player_id'].append(p['penalty_player_id'])
		        self.mpd['penalty_player_name'].append(p['penalty_player_name'])

		        # get sack info
		        s = get_sack(details['players'])
		        self.mpd['sack'].append(s['sack'])
		        self.mpd['sack_player_id'].append(s['sack_pid'])
		        self.mpd['sack_player_name'].append(s['sack_name'])

		        # get touchdown info
		        tds = get_touchdowns(details['players'])
		        self.mpd['touchdown'].append(tds['touchdown'])
		        self.mpd['pass_touchdown'].append(tds['pass_touchdown'])
		        self.mpd['rush_touchdown'].append(tds['rush_touchdown'])
		        self.mpd['return_touchdown'].append(tds['return_touchdown'])
		        self.mpd['td_team'].append(tds['td_team'])
		        if tds['touchdown'] == 1:
		            points_scored += 6
		            points_scored_team = tds['td_team']

		        # get special teams info
		        st = get_special_teams(self.mpd,idx,details['players'])
		        self.mpd['extra_point_attempt'].append(st['xp_att'])
		        self.mpd['two_point_attempt'].append(st['twopt_att'])
		        self.mpd['field_goal_attempt'].append(st['fg_att'])
		        self.mpd['kickoff_attempt'].append(st['kickoff_att'])
		        self.mpd['punt_attempt'].append(st['punt_att'])
		        self.mpd['field_goal_result'].append(st['field_goal_result'])
		        self.mpd['kick_distance'].append(st['kick_distance'])
		        self.mpd['extra_point_result'].append(st['extra_point_result'])
		        self.mpd['two_point_conv_result'].append(st['two_point_conv_result'])
		        self.mpd['punt_returner_player_id'].append(st['punt_returner_player_id'])
		        self.mpd['punt_returner_player_name'].append(st['punt_returner_player_name'])
		        self.mpd['kickoff_returner_player_name'].append(st['kickoff_returner_player_name'])
		        self.mpd['kickoff_returner_player_id'].append(st['kickoff_returner_player_id'])
		        self.mpd['punter_player_id'].append(st['punter_player_id'])
		        self.mpd['punter_player_name'].append(st['punter_player_name'])
		        self.mpd['kicker_player_name'].append(st['kicker_player_name'])
		        self.mpd['kicker_player_id'].append(st['kicker_player_id'])
		        self.mpd['blocked_player_id'].append(st['blocked_player_id'])
		        self.mpd['blocked_player_name'].append(st['blocked_player_name'])
		        self.mpd['defensive_two_point_attempt'].append(st['defensive_two_point_attempt'])
		        self.mpd['defensive_two_point_conv'].append(st['defensive_two_point_conv'])
		        self.mpd['defensive_extra_point_attempt'].append(st['defensive_extra_point_attempt'])
		        self.mpd['defensive_extra_point_conv'].append(st['defensive_extra_point_conv'])
		        points_scored += st['points_scored']
		        if st['sp_team'] != 'N/A':
		            points_scored_team = st['sp_team']

		        # get turnovers
		        to = get_turnovers(details['players'])
		        self.mpd['fumble'].append(to['fumble'])
		        self.mpd['fumble_forced'].append(to['fumble_forced'])
		        self.mpd['fumble_not_forced'].append(to['fumble_not_forced'])
		        self.mpd['fumble_out_of_bounds'].append(to['fumble_out_of_bounds'])
		        self.mpd['fumble_lost'].append(to['fumble_lost'])
		        self.mpd['interception'].append(to['interception'])
		        self.mpd['interception_player_id'].append(to['interception_player_id'])
		        self.mpd['interception_player_name'].append(to['interception_player_name'])
		        self.mpd['forced_fumble_player_1_team'].append(to['forced_fumble_player_1_team'])
		        self.mpd['forced_fumble_player_1_player_id'].append(to['forced_fumble_player_1_player_id'])
		        self.mpd['forced_fumble_player_1_player_name'].append(to['forced_fumble_player_1_player_name'])
		        self.mpd['forced_fumble_player_2_team'].append(to['forced_fumble_player_2_team'])
		        self.mpd['forced_fumble_player_2_player_id'].append(to['forced_fumble_player_2_player_id'])
		        self.mpd['forced_fumble_player_2_player_name'].append(to['forced_fumble_player_2_player_name'])
		        self.mpd['fumbled_1_team'].append(to['fumbled_1_team'])
		        self.mpd['fumbled_1_player_id'].append(to['fumbled_1_player_id'])
		        self.mpd['fumbled_1_player_name'].append(to['fumbled_1_player_name'])
		        self.mpd['fumbled_2_player_id'].append(to['fumbled_2_player_id'])
		        self.mpd['fumbled_2_player_name'].append(to['fumbled_2_player_name'])
		        self.mpd['fumbled_2_team'].append(to['fumbled_2_team'])
		        self.mpd['fumble_recovery_1_team'].append(to['fumble_recovery_1_team'])
		        self.mpd['fumble_recovery_1_yards'].append(to['fumble_recovery_1_yards'])
		        self.mpd['fumble_recovery_1_player_id'].append(to['fumble_recovery_1_player_id'])
		        self.mpd['fumble_recovery_1_player_name'].append(to['fumble_recovery_1_player_name'])
		        self.mpd['fumble_recovery_2_team'].append(to['fumble_recovery_2_team'])
		        self.mpd['fumble_recovery_2_yards'].append(to['fumble_recovery_2_yards'])
		        self.mpd['fumble_recovery_2_player_id'].append(to['fumble_recovery_2_player_id'])
		        self.mpd['fumble_recovery_2_player_name'].append(to['fumble_recovery_2_player_name'])

		        # get pass info
		        off = get_pass_info(details['players'],details['desc'])
		        self.mpd['pass_attempt'].append(off['pass_att'])
		        self.mpd['complete_pass'].append(off['complete_pass'])
		        self.mpd['incomplete_pass'].append(off['incomplete_pass'])
		        self.mpd['passer_player_id'].append(off['passer_pid'])
		        self.mpd['passer_player_name'].append(off['passer_name'])
		        self.mpd['receiver_player_id'].append(off['receiver_pid'])
		        self.mpd['receiver_player_name'].append(off['receiver_name'])
		        self.mpd['pass_length'].append(off['pass_length'])
		        self.mpd['pass_location'].append(off['pass_location'])
		        self.mpd['air_yards'].append(off['air_yards'])
		        self.mpd['yards_after_catch'].append(off['yards_after_catch'])

		        # get rush info
		        r = get_rush_info(details['players'],details['desc'])
		        self.mpd['rush_attempt'].append(r['rush_att'])
		        self.mpd['rusher_player_id'].append(r['rusher_pid'])
		        self.mpd['rusher_player_name'].append(r['rusher_name'])
		        self.mpd['run_location'].append(r['run_location'])
		        self.mpd['run_gap'].append(r['run_gap'])

		        # get yards gained
		        if to['fumble_lost'] > 0 or to['interception'] > 0:
		            self.mpd['yards_gained'].append(0)
		        else:
		            self.mpd['yards_gained'].append(get_yards_gained(details['players'])+p['penalty_yards']+st['two_point_yds_gained'])

		        # get qb action
		        qba = get_qb_action(details['desc'])
		        self.mpd['qb_kneel'].append(qba['qb_kneel'])
		        self.mpd['qb_spike'].append(qba['qb_spike'])
		        self.mpd['qb_scramble'].append(qba['qb_scramble'])
		        self.mpd['shotgun'].append(qba['shotgun'])
		        self.mpd['no_huddle'].append(qba['no_huddle'])
		        if off['pass_att'] == 1 or (r['rush_att'] == 1 and qba['qb_scramble'] == 1):
		            self.mpd['qb_dropback'].append(1)
		        else:
		            self.mpd['qb_dropback'].append(0)

		        # get play type
		        play_type = get_play_type(self.mpd,idx)
		        self.mpd['play_type'].append(play_type)

		        # get points scored
		        ps = {
		            'home_team_score' : home_team_score,
		            'away_team_score' : away_team_score,
		            'posteam' : details['posteam'],
		            'home_team' : self.mpd['home_team'],
		            'away_team' : self.mpd['away_team'],
		            'sp' : details['sp'],
		            'points_scored_team' : points_scored_team,
		            'points_scored' : points_scored,
		        }
		        psn = get_points_scored(ps)
		        self.mpd['total_home_score'].append(psn['home_team_score'])
		        self.mpd['total_away_score'].append(psn['away_team_score'])
		        self.mpd['posteam_score'].append(psn['posteam_score'])
		        self.mpd['defteam_score'].append(psn['defteam_score'])
		        self.mpd['score_differential'].append(psn['score_differential'])
		        self.mpd['posteam_score_post'].append(psn['posteam_score_post'])
		        self.mpd['defteam_score_post'].append(psn['defteam_score_post'])
		        self.mpd['score_differential_post'].append(psn['score_differential_post'])
		        home_team_score = psn['home_team_score_post']
		        away_team_score = psn['away_team_score_post']

		        # get defensive info
		        defense = get_defensive_stats(details['players'])
		        self.mpd['safety'].append(defense['safety'])
		        self.mpd['tackled_for_loss'].append(defense['tackled_for_loss'])
		        self.mpd['qb_hit'].append(defense['qb_hit'])
		        self.mpd['tackle_for_loss_1_player_id'].append(defense['tackle_for_loss_1_player_id'])
		        self.mpd['tackle_for_loss_1_player_name'].append(defense['tackle_for_loss_1_player_name'])
		        self.mpd['tackle_for_loss_2_player_id'].append(defense['tackle_for_loss_2_player_id'])
		        self.mpd['tackle_for_loss_2_player_name'].append(defense['tackle_for_loss_2_player_name'])
		        self.mpd['qb_hit_1_player_id'].append(defense['qb_hit_1_player_id'])
		        self.mpd['qb_hit_1_player_name'].append(defense['qb_hit_1_player_name'])
		        self.mpd['qb_hit_2_player_id'].append(defense['qb_hit_2_player_id'])
		        self.mpd['qb_hit_2_player_name'].append(defense['qb_hit_2_player_name'])
		        self.mpd['pass_defense_1_player_id'].append(defense['pass_defense_1_player_id'])
		        self.mpd['pass_defense_1_player_name'].append(defense['pass_defense_1_player_name'])
		        self.mpd['pass_defense_2_player_id'].append(defense['pass_defense_2_player_id'])
		        self.mpd['pass_defense_2_player_name'].append(defense['pass_defense_2_player_name'])
		        self.mpd['return_team'].append(defense['return_team'])
		        self.mpd['return_yards'].append(defense['return_yards'])

		        idx += 1
		self.mpd = pd.DataFrame.from_dict(self.mpd)
		self.mpd = self.mpd[TableColumns().nflapi['pbp_cols']]
		return self.mpd
