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

link = "https://www.pro-football-reference.com/boxscores/201310270den.htm"
page_soup = get_soup(link)
pbp_data = get_data("all_pbp",1)
all_quarters = pbp_data.findAll("th",{"data-stat":"quarter"})
all_timeremain = pbp_data.findAll("td",{"data-stat":"qtr_time_remain"})
all_playdetail = pbp_data.findAll("td",{"data-stat":"detail"})
