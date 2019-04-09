import re
import sys
import bs4
import xlsxwriter
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from workbooks import generate_workbook
from analyze_play import Play

# returns page soup object
def get_soup_create_file(link):
    uClient = uReq(link)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "lxml")
    f = open('page_soup.html','w')
    encodedsoup = (page_soup.encode('utf-8').strip())
    f.write(str(encodedsoup))
    f.close()
    return page_soup

def get_soup(link):
    page_soup = soup(open(link), "lxml")
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

#------------------------------------#
#------------ BEGIN MAIN ------------#
#------------------------------------#

### set global variables ###
#--------------------------#
workbook,worksheets = generate_workbook('demo2.xlsx')
gameid = '/boxscores/201310270den.htm'

### scrape data ###
#-----------------#
link = "page_soup.html"
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

rownum = {
    "PASS":1,
    "RUSH":1,
    "DEF":1,
    "ST":1,
    "PENALTY":1,
    "MISC":1
}

### process scraped data ###
#--------------------------#
for idx,val in enumerate(all_playdetails):
# idx = 19
# for x in range(1):
    playnum = idx+1
    if re.search(r'\D',all_quarters[idx].text):
        all_quarters.pop(idx)
    play_details = Play(all_playdetails[idx],workbook,worksheets,playnum,rownum)
    print(all_quarters[idx].text+"-"+all_timeremain[idx].text+" ["+str(playnum)+"]")
    play_details.analyze_play()
    rownum = play_details.rownum
    worksheets['PLAYS'].write(playnum,0,playnum)
    worksheets['PLAYS'].write(playnum,1,gameid)
    worksheets['PLAYS'].write(playnum,2,all_quarters[idx].text)
    worksheets['PLAYS'].write(playnum,3,all_timeremain[idx].text)
    worksheets['PLAYS'].write(playnum,4,all_downs[idx].text)
    worksheets['PLAYS'].write(playnum,5,all_ydstogo[idx].text)
    worksheets['PLAYS'].write(playnum,6,all_locations[idx].text)
    worksheets['PLAYS'].write(playnum,7,all_playdetails[idx].text)
    worksheets['PLAYS'].write(playnum,8,all_scores_home[idx].text)
    worksheets['PLAYS'].write(playnum,9,all_scores_away[idx].text)
    worksheets['PLAYS'].write(playnum,10,all_epb[idx].text)
    worksheets['PLAYS'].write(playnum,11,all_epa[idx].text)

workbook.close()
