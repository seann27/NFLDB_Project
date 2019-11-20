import re
from scrapers.GeneralScraper import Scraper

class ApiGameLinks:

	def __init__(self,season,week):
		self.baseurl = 'http://www.nfl.com/schedules/'+str(season)+'/reg'+str(week)
		self.basesoup = Scraper(self.baseurl).get_soup()

	def get_gamelinks(self):
		self.gamelinks = []
		links = self.basesoup.findAll("div",{"data-gameid":re.compile(r'[0-9]{10}')})
		for link in links:
		    gameid = link['data-gameid']
		    self.gamelinks.append("http://www.nfl.com/liveupdate/game-center/"+str(gameid)+'/'+str(gameid)+"_gtd.json")
		return self.gamelinks

	def get_gameids(self):
		self.gameids = []
		links = self.basesoup.findAll("div",{"data-gameid":re.compile(r'[0-9]{10}')})
		for link in links:
		    self.gameids.append(link['data-gameid'])
		return self.gameids