import re
import sys
import numpy as np
import pandas as pd
import bs4
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from references_dict import Team_Dictionary,DataFrameColumns

from analyze_play import Play

# utiliy methods
def get_soup(link):
    page_soup = soup(open(link), "lxml")
    return page_soup

# utility method for parsing game page tables
def get_data(page_soup,id,commented=0):
    data = page_soup.find("div",{"id":id})
    if commented > 0:
        comment = data.find(string=lambda text:isinstance(text,Comment))
        data = soup(comment,"lxml")
    players = [tr.find("th",{"scope":"row"}) for tr in data.findAll("tr",{"class":None})]
    stats = [tr.findAll("td") for tr in data.findAll("tr",{"class":None})]
    players.pop(0)
    stats.pop(0)
    return players,stats

def get_pbp_data():
    data = page_soup.find("div",{"id":'all_pbp'})
    comment = data.find(string=lambda text:isinstance(text,Comment))
    data = soup(comment,"lxml")
    return data

def insert_sql(table,metrics):
    columns = DataFrameColumns().football_ref[table]
    metrics = np.asarray(metrics)
    df = pd.DataFrame(metrics,columns=columns)
    # print(table)
    # print(df)
    # print()
    return df

# classes
class GameInfo():
    def __init__(self,gameid,home,away):
        self.game_id = gameid
        self.home_id = home
        self.away_id = away

    def get_opponent(self,team):
        if team == self.home_name:
            return self.away_name
        else:
            return self.home_name

class Player():
    def __init__(self,player_id,player_name):
        self.player_id = player_id
        self.player_name = player_name

# scraper submethods
def scrape_game_info(page_soup):
    gameteams = page_soup.findAll("a",{"itemprop":"name"})
    gameinfo = GameInfo(gameid,gameteams[0]['href'],gameteams[1]['href'])
    gameinfo.home_name = gameteams[0].text
    gameinfo.away_name = gameteams[1].text
    game_information = page_soup.find("div",{"id":"all_game_info"})
    comment = game_information.find(string=lambda text:isinstance(text,Comment))
    game_information = soup(comment,"lxml")
    game_information = [tr.findAll("td") for tr in game_information.findAll("tr",{"class":None})]
    vegasline = game_information[-2][0].text.strip()
    vegasline = re.split("\s-",vegasline)
    if vegasline[0] == gameinfo.away_id:
        vegasline = vegasline[1]*-1
    else:
        vegasline = vegasline[1]
    overunder = float(game_information[-1][0].text.split(" ")[0].strip())
    score = page_soup.findAll("div",{"class":"score"})
    points_home = float(score[0].text.strip())
    points_away = float(score[1].text.strip())
    values = [[
    	gameid,
        season,
        week,
        gameinfo.home_id,
        points_home,
        gameinfo.away_id,
        points_away,
        vegasline,
        overunder
    ]]
    df = insert_sql('GAMEINFO',values)
    return gameinfo,df

# get position, snapcounts to player objects
def scrape_snapcounts(home_team,away_team,page_soup):
    relevant_positions = ('QB','WR','RB','TE')
    metrics = []
    player_team_dict = {}
    def parse_players(metrics,team,players,stats):
        for player,stat in zip(players,stats):
            playerid = player.a['href']
            name = player.text
            position = stat[0].text
            team = team
            player_team_dict[playerid] = team
            snapcount_off = stat[1].text
            pct_snaps_off = float(stat[2].text.strip('%'))
            if position in relevant_positions:
                metrics.append([gameid,playerid,name,position,team,snapcount_off,pct_snaps_off])
    home_players,home_stats = get_data(page_soup,"all_home_snap_counts",1)
    away_players,away_stats = get_data(page_soup,"all_vis_snap_counts",1)
    parse_players(metrics,home_team,home_players,home_stats)
    parse_players(metrics,away_team,away_players,away_stats)
    df = insert_sql('SNAPCOUNTS',metrics)
    return df,player_team_dict

def scrape_offensive_stats(section,table,page_soup):
    metrics = []
    players,stats = get_data(page_soup,section,1)
    for player,stat in zip(players,stats):
        metric_list = [gameid]
        metric_list.append(player.text)
        for metric in stat:
            value = metric.text
            if not value:
                value = 0
            metric_list.append(value)
        metrics.append(metric_list)
    df = insert_sql(table,metrics)
    return df

def scrape_defensive_stats(home_name,away_name,player_team_dict,page_soup):
    # define stats dictionary
    team_stats = {
        home_name: [gameid,home_name,0,0,0,0,0,0],
        away_name: [gameid,away_name,0,0,0,0,0,0]
    }

    # scrape summary defense stats
    players,stats = get_data(page_soup,'all_player_defense',1)
    for stat in stats:
        team = Team_Dictionary().football_ref[stat[0].text]
        team_stats[team][3] += float(stat[1].text)
        team_stats[team][2] += float(stat[6].text)
        team_stats[team][4] += float(stat[12].text)
        team_stats[team][5] += float(stat[3].text)
        team_stats[team][5] += float(stat[14].text)

    # find all instances of where a blocked punt/fg has occurred
    pbp_data = get_pbp_data()
    all_playdetails = pbp_data.findAll("td",{"data-stat":"detail"})
    for play in all_playdetails:
        blocked = re.search('blocked',play.text)
        testing = re.search('extra point good',play.text)
        if blocked:
            player_tags = play.findAll('a')
            player_tags.pop(0)
            playerid = player_tags[0]['href']
            team = player_team_dict[playerid]
            if team == home_name:
                team = away_name
            else:
                team == home_name
            team_stats[team][7] += 1

    # calculate how many 2-point plays happened
    home_team_score = 0
    away_team_score = 0
    misc,stats = get_data(page_soup,'all_scoring')
    for stat in stats:
        home_score = int(stat[4].text)
        away_score = int(stat[3].text)
        if (home_score - home_team_score) == 2:
            team_stats[home_name][6] += 1
        if (away_score - away_team_score) == 2:
            team_stats[away_name][6] += 1
        home_team_score = home_score
        away_team_score = away_score

    # convert stats dictionary to dataframe
    defense_metrics = [team_stats[home_name],team_stats[away_name]]
    metrics = np.asarray(defense_metrics)
    df = insert_sql('DST',metrics)
    return df

file = "sqlcommands.txt"
command_file = open(file,"w")
gameid = '/boxscores/201310270den.htm'
season = 2013
week = 8
link = "page_soup.html"
page_soup = get_soup(link)
gameinfo,gameinfo_df = scrape_game_info(page_soup)
snapcounts_df,player_team_dict = scrape_snapcounts(gameinfo.home_name,gameinfo.away_name,page_soup)
all_offense_df = scrape_offensive_stats('all_player_offense','ALL_OFF',page_soup)
detailed_receiving_df = scrape_offensive_stats('all_targets_directions','REC',page_soup)
detailed_rushing_df = scrape_offensive_stats('all_rush_directions','RUSH',page_soup)
summary_defense_df = scrape_defensive_stats(gameinfo.home_name,gameinfo.away_name,player_team_dict,page_soup)
print('GAMEINFO')
print(gameinfo_df)
print()
print('ALL OFFENSE')
print(all_offense_df)
print()
print('RECEIVING')
print(detailed_receiving_df)
print()
print('RUSHING')
print(detailed_rushing_df)
print()
print('DEFENSE')
print(summary_defense_df)
print()
