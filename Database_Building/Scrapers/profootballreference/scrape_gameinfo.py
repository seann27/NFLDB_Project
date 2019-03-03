import mysql.connector
import logging
import datetime
import re
import sys
import bs4
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq
from team_dictionary import Team_Dictionary

# # initialize logger
# timeid = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# logfile = ('logs/run_SQL_DRIVER_'+timeid+'.log')
# logging.basicConfig(level=logging.DEBUG,filename=logfile,filemode='w',format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')
#
# # initialize db connection
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="",
#   database="nfl_db"
# )
#
# mycursor = mydb.cursor()

def get_soup(link):
    uClient = uReq(link)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "lxml")
    return page_soup

season = 2018
week = 15

link = "https://www.pro-football-reference.com/years/2018/week_"+str(week)+".htm"
page_soup = get_soup(link)
games = page_soup.findAll("td",{"class":"gamelink"})

for game in games:
	player_list = {}
	link = "https://www.pro-football-reference.com"+str(game.a['href'])
	print()
	print("Accessing game "+link)
	page_soup = get_soup(link)
