#!/usr/bin/python

import re
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def getRoster(link):
	players = {}

	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html,"html.parser")

	containers = page_soup.findAll("span",{"style":"min-width:140px"})
	roster_size = 0
	for line in containers:
		x = line.a
		try: x
		except NameError: x = None

		if x is None:
			continue
		else:
			soup_string = str(x)
			if re.match(r".+http://www.espn.com/nfl/player/_/id/(\d+)",soup_string):
				m = re.match(r".+(http://www.espn.com/nfl/player/_/id/)(\d+)",soup_string)
				# print(m.group(1)+m.group(2))
				id = m.group(2).strip()
				player_name = x.text
				player_name = player_name.strip()
				players[id] = player_name
	return players

class Player:

	def __init__(self,link):
		self.link = link
		uClient = uReq(link)
		page_html = uClient.read()
		uClient.close()
		page_soup = soup(page_html,"html.parser")
		general_info = page_soup.find("ul",{"class":"general-info"})
		attributes = general_info.findAll("li")
		self.position = attributes[0].text
		self.physical = attributes[1].text
