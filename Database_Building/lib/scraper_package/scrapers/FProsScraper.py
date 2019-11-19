import pandas as pd
import numpy as np
import re
from scrapers.GeneralScraper import Scraper
from NFL_RefMaps import TableColumns,TeamDictionary

class LoadProjections:

	def __init__(self,week):

		self.week = week
		self.projections = self.get_all_projections()

	def get_projections(self,pos):
		link = "https://www.fantasypros.com/nfl/projections/"+pos+".php?week="+str(self.week)+"&scoring=HALF"
		page_soup = Scraper(link).get_soup()
		data = page_soup.find("tbody")

		table = pos+'_projections'
		metrics = [TableColumns().fantasy_pros[table]]
		players = data.findAll("tr",{"class":re.compile(r'mpb-player-')})
		for player in players:
			stats = player.findAll("td")
			name = stats[0].a.text
			team = 'n/a'
			if pos == 'dst':
				team = TeamDictionary().nfl_api[name]
			else:
				err = stats[0].text.strip().split()
				if len(err) == 0:
					print("Error detected in ",link," ... skipping row")
					break
				team = stats[0].text.strip().split()[-1]
			a = stats[0].findAll("a")
			pid = a[1].get('class')[1]
			mets = np.array([pid,name,team,self.week])
			for stat in stats[1:]:
				mets = np.append(mets,stat.text)
			metrics.append(mets)
		df = np.vstack(metrics)
		return pd.DataFrame(data=df[1:,1:],index=df[1:,0],columns=df[0,1:])

	def get_all_projections(self):
		projections = {
			'qb':'',
			'rb':'',
			'wr':'',
			'te':'',
			'dst':'',
			'k':''
		}
		for key,val in projections.items():
			projections[key] = self.get_projections(key)

		return projections

class LoadRankings:

	def __init__(self):

		self.week = week
		self.rankings = self.get_all_rankings()

	def get_rankings(self,pos):
		half = [ 'rb','wr','te','flex' ]
		standard = [ 'qb','k','dst' ,'idp','dl','lb','db']
		link = "https://www.fantasypros.com/nfl/rankings/"
		if pos in half:
			link += "half-point-ppr-"
		link += pos+".php?week="+str(self.week)
		page_soup = Scraper(link).get_soup()
		data = page_soup.find("tbody")

		metrics = [TableColumns().fantasy_pros['rankings']]
		players = data.findAll("tr",{"class":re.compile(r'mpb-player-')})
		for player in players:
			stats = player.findAll("td")
			name = stats[0].a.text
			team = 'n/a'
			if pos == 'dst':
				team = TeamDictionary().nfl_api[name]
			else:
				err = stats[0].text.strip().split()
				if len(err) == 0:
					print("Error detected in ",link," ... skipping row")
					break
				team = stats[0].text.strip().split()[-1]
			a = stats[0].findAll("a")
			pid = a[1].get('class')[1]
			mets = np.array([pid,name,team,self.week])
			for stat in stats[1:]:
				mets = np.append(mets,stat.text)
			metrics.append(mets)
		df = np.vstack(metrics)
		return pd.DataFrame(data=df[1:,1:],index=df[1:,0],columns=df[0,1:])

	def get_all_rankings(self):
		rankings = {
			'qb':'',
			'rb':'',
			'wr':'',
			'te':'',
			'flex':'',
			'k':'',
			'dst' :'',
			'idp':'',
			'dl':'',
			'lb':'',
			'db':''
		}
		for key,val in rankings.items():
			rankings[key] = self.get_rankings(key)

		return rankings
