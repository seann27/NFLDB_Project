import re
from scrapers.GeneralScraper import Scraper

class ApiGameLinks:

	def __init__(self,season,week):
		self.baseurl = 'http://www.nfl.com/schedules/'+str(season)
		if week < 18:
			self.baseurl += '/REG'+str(week)
		else:
			self.baseurl += '/POST'
		self.basesoup = Scraper(self.baseurl).get_soup()

		playoffs = {
			'18':[0,4],
			'19':[4,8],
			'20':[8,10],
			'21':[10,11],
			'22':[11,12]
		}
		if week > 17:
			self.selected_games = playoffs[str(week)]
		else:
			self.selected_games is None

	def get_gamelinks(self):
		self.gamelinks = []
		links = self.basesoup.findAll("div",{"data-gameid":re.compile(r'[0-9]{10}')})
		for link in links:
		    gameid = link['data-gameid']
		    self.gamelinks.append("http://www.nfl.com/liveupdate/game-center/"+str(gameid)+'/'+str(gameid)+"_gtd.json")

		if self.selected_games:
			current = 0
			if len(self.gamelinks) == 13:
				current = 1
			self.gamelinks = self.gamelinks[(selected_games[0]+current):(selected_games[1]+current)]

		return self.gamelinks

	def get_gameids(self):
		self.gameids = []
		links = self.basesoup.findAll("div",{"data-gameid":re.compile(r'[0-9]{10}')})
		for link in links:
		    self.gameids.append(link['data-gameid'])

		if self.selected_games:
			current = 0
			if len(self.gameids) == 13:
				current = 1
			self.gameids = self.gameids[(self.selected_games[0]+current):(self.selected_games[1]+current)]

		return self.gameids
