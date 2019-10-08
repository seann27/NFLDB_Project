from .GeneralScraper import Scraper
from NFL_RefMaps import TableColumns

class PFR(Scraper):

	def __init__(self,link):
		Scraper.__init__(self,link)
		self.page_soup = self.get_soup()

	# utility method for parsing game page tables
	def get_data(self,id,commented=0):
	    data = self.page_soup.find("div",{"id":id})
	    if commented > 0:
	        comment = data.find(string=lambda text:isinstance(text,Comment))
	        data = soup(comment,"lxml")
	    players = [tr.find("th",{"scope":"row"}) for tr in data.findAll("tr",{"class":None})]
	    stats = [tr.findAll("td") for tr in data.findAll("tr",{"class":None})]
	    players.pop(0)
	    stats.pop(0)
	    return players,stats

	# utiliy method to dynamically scrape tables
	def get_pfr_table(self,table):
	    gameid = self.link.split('boxscores/')[1].split('.')[0]
	    metrics = [TableColumns().football_ref[table]]
	    players,stats = self.get_data(table,1)
	    for player,stat in zip(players,stats):
	        mets = np.array([gameid,player.a['href'],player.text])
	        for idx,metric in enumerate(stat):
	            value = metric.text
	            if not value:
	                value = 0
	            if idx > 0 and '%' not in metric.text:
	                value = float(value)
	            mets = np.append(mets,value)
	        metrics.append(mets)
	    df = np.vstack(metrics)
	    return pd.DataFrame(data=df[1:,1:],index=df[1:,0],columns=df[0,1:])

	def get_total_offense(self):
	    return self.get_pfr_table('all_player_offense')

	def get_receiving(self):
	    return self.get_pfr_table('all_targets_directions')

	def get_rushing(self):
	    return self.get_pfr_table('all_rush_directions')

	def get_defense(self):
	    return self.get_pfr_table('all_player_defense')

	def get_returns(self):
	    return self.get_pfr_table('all_returns')

	def get_home_snapcounts(self):
	    return self.get_pfr_table('all_home_snap_counts')

	def get_vis_snapcounts(self):
	    return self.get_pfr_table('all_vis_snap_counts')

	def get_gameinfo(self):
	    link_comps = self.link.split('boxscores/')
	    link_comps = link_comps[1].split('.')
	    gameid = link_comps[0]
	    date = gameid[:8]

	    # get team names
	    gameteams = self.page_soup.findAll("a",{"itemprop":"name"})
	    team_home = gameteams[0].text
	    team_away = gameteams[1].text

	    # get vegas odds
	    gameinfo = self.page_soup.find("div",{"id":"all_game_info"})
	    comment = gameinfo.find(string=lambda text:isinstance(text,Comment))
	    gameinfo = soup(comment,"lxml")
	    gameinfo = [tr.findAll("td") for tr in gameinfo.findAll("tr",{"class":None})]
	    vegasline = gameinfo[-2][0].text.strip()
	    vegasline = re.split("\s-",vegasline)
	    print(vegasline)
	    home_fav = 1
	    if vegasline[0] == team_away:
	        home_fav = 0
	    vegasline = float(vegasline[1])
	    overunder = float(gameinfo[-1][0].text.split(" ")[0].strip())
	    print('home_fav = ',home_fav,', ats = ',vegasline,', ou = ',overunder)

	    # get score
	    score = self.page_soup.findAll("div",{"class":"score"})
	    points_home = float(score[0].text.strip())
	    points_away = float(score[1].text.strip())
	    home_score_diff = points_home - points_away
	    print('score_diff = ',home_score_diff)

	    # calculate vegas results
	    ats_result = 0
	    if((home_score_diff > vegasline and home_fav == 1) or (home_score_diff < (vegasline*-1) and home_fav == 0)):
	        ats_result = 1
	    elif((home_score_diff < vegasline and home_fav == 1) or (home_score_diff > (vegasline*-1) and home_fav == 0)):
	        ats_result = -1

	    ou_result = 0
	    if(points_home+points_away > overunder):
	        ou_result = 1
	    elif(points_home+points_away < overunder):
	        ou_result = -1

	    # return metrics in numpy array
	    stats = np.array([gameid,date,team_home,points_home,team_away,points_away,home_fav,vegasline,overunder,ats_result,ou_result])
	    return stats

	def get_game_links(self):
		games = []
		game_links = self.page_soup.findAll("td",{"class":"gamelink"})
		for game in game_links:
			gameid = (str(game.a['href']))
	        date = gameid[11:20]
	        link = "https://www.pro-football-reference.com"+gameid
		return games

	def get_gameid(self,link):
		if len(link) < 38:
			return "Error! Length of input link not long enough!"
		else:
			return link[38:]

	def get_gamedate(self,link):
		if len(link) < 58:
			return "Error! Length of input link not long enough!"
		else:
			return link[49:57]
