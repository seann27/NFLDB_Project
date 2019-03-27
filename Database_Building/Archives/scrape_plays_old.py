import re
import sys
import bs4
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq

# returns page soup object
def get_soup(link):
    uClient = uReq(link)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "lxml")
    return page_soup

# utility method for parsing game page tables
def get_data(id,commented=0):
    data = page_soup.find("div",{"id":id})
    # print(". . . getting data for table id: "+id)
    if commented > 0:
        # print(". . . processing as comment...")
        comment = data.find(string=lambda text:isinstance(text,Comment))
        data = soup(comment,"lxml")
    return data

def analyze_play(play):
    type = ''   # timeout, challenge, penalty, kickoff, punt, fg, xp,
    location = 'null'
    qb = 'null'
    flex = 'null'
    def_plyr1 = 'null'
    def_plyr2 = 'null'

    result = 'null' # pass->(complete, incomplete),run->(gain, no gain),timeout/penalty->(no play),challenge->(upheld,reversed)
    # defensive stoppage -> (sack,tackle,defended,intercepted,fumble recovered)
    yards = 0
    points_scored = 0
    rawplay = str(play)
    play = play.text

    if re.search(r'Touchdown',play):
        points_scored = 6

    if re.search(r'Timeout',play):
        type = 'TIMEOUT'
    elif re.search(r'challenge',play):
        type = 'CHALLENGE'
    elif re.search(r'Penalty',play):
        type = 'PENALTY'
    elif re.search(r'kicks (off|onside)',play):
        type = 'KICKOFF'
    elif re.search(r'punts',play):
        type = 'PUNT'
        result = re.match(".*(\d+) yards",play)
        result = result.groups()[0]
    elif re.search(r'field goal',play):
        type = 'FG'
        if re.search(r'no good',play):
            result = 'NO GOOD'
        else:
            result = re.match(".*(\d+) yard",play)
            result = result.groups()[0]
            points_scored += 3
    elif re.search(r'kicks extra point',play):
        type = 'XP'
        if re.search(r'no good',play):
            result = 'NO GOOD'
        else:
            result = 'GOOD'
            points_scored += 1
    elif re.search(r'pass',play):
        type = 'PASS'
        if re.search(r'incomplete',play):
            result = 'INCOMPLETE'
        elif re.search(r'for no gain',play):
            result = str(0)
        elif re.search(r'for [-]?(\d+) yards',play):
            result = re.match(".*for [-]?(\d+) yards",play)
            result = str(result.groups()[0])
    else:
        type = 'RUN'
        if re.search(r'(left|right|middle)',play):
            location = re.match(".*((left|right)\s(end|tackle|guard)|(middle))",play)
            location = str(location.groups()[0])
        if re.search(r'for no gain',play):
            result = str(0)
        elif re.search(r'for [-]?(\d+) yards',play):
            result = re.match(".*for [-]?(\d+) yards",play)
            result = str(result.groups()[0])
    return type,result,location,points_scored

link = "https://www.pro-football-reference.com/boxscores/201310270den.htm"
# link = "https://www.pro-football-reference.com/boxscores/201310270min.htm"
page_soup = get_soup(link)
pbp_data = get_data("all_pbp",1)
all_quarters = pbp_data.findAll("th",{"data-stat":"quarter"})
all_timeremain = pbp_data.findAll("td",{"data-stat":"qtr_time_remain"})
all_downs = pbp_data.findAll("td",{"data-stat":"down"})
all_ydstogo = pbp_data.findAll("td",{"data-stat":"yds_to_go"})
all_locations = pbp_data.findAll("td",{"data-stat":"location"})
all_playdetails = pbp_data.findAll("td",{"data-stat":"detail"})
all_scores_away = pbp_data.findAll("td",{"data-stat":"pbp_score_aw"})
all_scores_home = pbp_data.findAll("td",{"data-stat":"pbp_score_hm"})
all_epb = pbp_data.findAll("td",{"data-stat":"exp_pts_before"})
all_epa = pbp_data.findAll("td",{"data-stat":"exp_pts_after"})

# print(len(all_quarters))
# print(len(all_timeremain))
# print(len(all_downs))
# print(len(all_ydstogo))
# print(len(all_locations))
# print(len(all_playdetails))
# print(len(all_scores_away))
# print(len(all_scores_home))
# print(len(all_epb))
# print(len(all_epa))

for idx,val in enumerate(all_playdetails):
# idx = 38
# for x in range(1):
    type,result,location,points_scored = analyze_play(all_playdetails[idx])
    # if playtype == 'RUN/PASS':
    #     continue
    if re.search(r'\D',all_quarters[idx].text):
        all_quarters.pop(idx)
    # print(all_quarters[idx].text+" | "+
    #       all_timeremain[idx].text+" | "+
    #       all_downs[idx].text+" | "+
    #       all_ydstogo[idx].text+" | "+
    #       all_locations[idx].text+" | "+
    #       all_playdetails[idx].text+" | "+
    #       type+","+result+","+location+","+str(points_scored)+" | "+
    #       all_scores_away[idx].text+" | "+
    #       all_scores_home[idx].text+" | "+
    #       all_epb[idx].text+" | "+
    #       all_epa[idx].text)
    playstat = (all_playdetails[idx].text+" | "+
          type+","+result+","+location+","+str(points_scored))
