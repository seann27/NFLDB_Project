from StatsScraper import ScrapeEspnProjections

season = 2018
current_week = 13
for i in range(current_week-1):
	week = i+1
	espn = ScrapeEspnProjections(season,week)
	espn.scrape()
