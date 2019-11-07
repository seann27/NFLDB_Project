from scrapers.GeneralScraper import Scraper

class GameLinks:

	def __init__(self,season,week):
		self.baseurl = 'http://www.nfl.com/schedules/'+str(season)+'/reg'+str(week)
		self.basesoup = Scraper(base_url).get_soup()

	def get_gamelinks(self):
		self.gamelinks = []
		links = self.basesoup.findAll("div",{"data-gameid":re.compile(r'[0-9]{10}')})
		for link in links:
		    gameid = link['data-gameid']
		    self.gamelinks.append("http://www.nfl.com/liveupdate/game-center/"+str(gameid)+'/'+str(gameid)+"_gtd.json")
		return self.gamelinks
