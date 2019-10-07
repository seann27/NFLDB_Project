from .GeneralScraper import Scraper

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

class Team_Dictionary:
	def __init__(self):
		self.kaggle_abbrev = {
			'Pittsburgh Steelers':'PIT',
			'Arizona Cardinals':'ARI',
			'Atlanta Falcons':'ATL',
			'Baltimore Ravens':'BAL',
			'Carolina Panthers':'CAR',
			'Cincinnati Bengals':'CIN',
			'Cleveland Browns':'CLE',
			'Green Bay Packers':'GB',
			'Houston Texans':'HOU',
			'Indianapolis Colts':'IND',
			'New Orleans Saints':'NO',
			'New York Giants':'NYG',
			'Seattle Seahawks':'SEA',
			'Tampa Bay Buccaneers':'TB',
			'New England Patriots':'NE',
			'Oakland Raiders':'OAK',
			'Buffalo Bills':'BUF',
			'Chicago Bears':'CHI',
			'Dallas Cowboys':'DAL',
			'Denver Broncos':'DEN',
			'Detroit Lions':'DET',
			'Jacksonville Jaguars':'JAX',
			'Kansas City Chiefs':'KC',
			'New York Jets':'NYJ',
			'Philadelphia Eagles':'PHI',
			'San Diego Chargers':'LAC',
			'San Francisco 49ers':'SF',
			'Tennessee Titans':'TEN',
			'Washington Redskins':'WAS',
			'Miami Dolphins':'MIA',
			'Minnesota Vikings':'MIN',
			'St. Louis Rams':'LAR',
			'Los Angeles Rams':'LAR',
			'Los Angeles Chargers':'LAC',
			'Houston Oilers':'HOU'
		}
		self.fantasy_pros = {
			'KC':'Kansas City Chiefs',
			'BAL':'Baltimore Ravens',
			'PIT':'Pittsburgh Steelers',
			'OAK':'Oakland Raiders',
			'NO':'New Orleans Saints',
			'TB':'Tampa Bay Buccaneers',
			'LAC':'Los Angeles Chargers',
			'CIN':'Cincinnati Bengals',
			'CAR':'Carolina Panthers',
			'CLE':'Cleveland Browns',
			'SEA':'Seattle Seahawks',
			'MIN':'Minnesota Vikings',
			'GB':'Green Bay Packers',
			'ATL':'Atlanta Falcons',
			'IND':'Indianapolis Colts',
			'HOU':'Houston Texans',
			'NE':'New England Patriots',
			'MIA':'Miami Dolphins',
			'LAR':'Los Angeles Rams',
			'STL':'St. Louis Rams',
			'CHI':'Chicago Bears',
			'DAL':'Dallas Cowboys',
			'PHI':'Philadelphia Eagles',
			'BUF':'Buffalo Bills',
			'NYJ':'New York Jets',
			'DET':'Detroit Lions',
			'ARI':'Arizona Cardinals',
			'DEN':'Denver Broncos',
			'SF':'San Francisco 49ers',
			'NYG':'New York Giants',
			'WAS':'Washington Redskins',
			'TEN':'Tennessee Titans',
			'JAC':'Jacksonville Jaguars'
		}
		self.rotoguru_abbrev = {
			'KAN':'Kansas City Chiefs',
			'BAL':'Baltimore Ravens',
			'PIT':'Pittsburgh Steelers',
			'OAK':'Oakland Raiders',
			'NO':'New Orleans Saints',
			'TAM':'Tampa Bay Buccaneers',
			'LAC':'Los Angeles Chargers',
			'CIN':'Cincinnati Bengals',
			'CAR':'Carolina Panthers',
			'CLE':'Cleveland Browns',
			'SEA':'Seattle Seahawks',
			'MIN':'Minnesota Vikings',
			'GB':'Green Bay Packers',
			'ATL':'Atlanta Falcons',
			'IND':'Indianapolis Colts',
			'HOU':'Houston Texans',
			'NE':'New England Patriots',
			'MIA':'Miami Dolphins',
			'LAR':'Los Angeles Rams',
			'CHI':'Chicago Bears',
			'DAL':'Dallas Cowboys',
			'PHI':'Philadelphia Eagles',
			'BUF':'Buffalo Bills',
			'NYJ':'New York Jets',
			'DET':'Detroit Lions',
			'ARI':'Arizona Cardinals',
			'DEN':'Denver Broncos',
			'SFO':'San Francisco 49ers',
			'NYG':'New York Giants',
			'WAS':'Washington Redskins',
			'TEN':'Tennessee Titans',
			'JAC':'Jacksonville Jaguars'
		}
		self.rotoguru_dsts = {
			'Arizona':'Arizona Cardinals',
			'Atlanta':'Atlanta Falcons',
			'Baltimore':'Baltimore Ravens',
			'Buffalo':'Buffalo Bills',
			'Carolina':'Carolina Panthers',
			'Chicago':'Chicago Bears',
			'Cincinnati':'Cincinnati Bengals',
			'Cleveland':'Cleveland Browns',
			'Dallas':'Dallas Cowboys',
			'Denver':'Denver Broncos',
			'Detroit':'Detroit Lions',
			'Green Bay':'Green Bay Packers',
			'Indianapolis':'Indianapolis Colts',
			'Jacksonville':'Jacksonville Jaguars',
			'Kansas City':'Kansas City Chiefs',
			'Miami':'Miami Dolphins',
			'Minnesota':'Minnesota Vikings',
			'New England':'New England Patriots',
			'New Orleans':'New Orleans Saints',
			'New York G':'New York Giants',
			'New York J':'New York Jets',
			'Oakland':'Oakland Raiders',
			'Philadelphia':'Philadelphia Eagles',
			'Pittsburgh':'Pittsburgh Steelers',
			'LA Rams':'Los Angeles Rams',
			'LA Chargers':'Los Angeles Chargers',
			'San Francisco':'San Francisco 49ers',
			'Seattle':'Seattle Seahawks',
			'Tampa Bay':'Tampa Bay Buccaneers',
			'Tennessee':'Tennessee Titans',
			'Washington':'Washington Redskins',
			'Houston':'Houston Texans'
		}
		self.espn_proj = {
			'KC':'Kansas City Chiefs',
			'BAL':'Baltimore Ravens',
			'PIT':'Pittsburgh Steelers',
			'OAK':'Oakland Raiders',
			'NO':'New Orleans Saints',
			'TB':'Tampa Bay Buccaneers',
			'LAC':'Los Angeles Chargers',
			'CIN':'Cincinnati Bengals',
			'CAR':'Carolina Panthers',
			'CLE':'Cleveland Browns',
			'SEA':'Seattle Seahawks',
			'MIN':'Minnesota Vikings',
			'GB':'Green Bay Packers',
			'ATL':'Atlanta Falcons',
			'IND':'Indianapolis Colts',
			'HOU':'Houston Texans',
			'NE':'New England Patriots',
			'MIA':'Miami Dolphins',
			'LAR':'Los Angeles Rams',
			'CHI':'Chicago Bears',
			'DAL':'Dallas Cowboys',
			'PHI':'Philadelphia Eagles',
			'BUF':'Buffalo Bills',
			'NYJ':'New York Jets',
			'DET':'Detroit Lions',
			'ARI':'Arizona Cardinals',
			'DEN':'Denver Broncos',
			'SF':'San Francisco 49ers',
			'NYG':'New York Giants',
			'WSH':'Washington Redskins',
			'TEN':'Tennessee Titans',
			'JAX':'Jacksonville Jaguars'
		}
		self.football_ref = {
			'ATL':'Atlanta Falcons',
			'PHI':'Philadelphia Eagles',
			'JAX':'Jacksonville Jaguars',
			'NYG':'New York Giants',
			'HOU':'Houston Texans',
			'NWE':'New England Patriots',
			'TAM':'Tampa Bay Buccaneers',
			'NOR':'New Orleans Saints',
			'SFO':'San Francisco 49ers',
			'MIN':'Minnesota Vikings',
			'TEN':'Tennessee Titans',
			'MIA':'Miami Dolphins',
			'CIN':'Cincinnati Bengals',
			'IND':'Indianapolis Colts',
			'PIT':'Pittsburgh Steelers',
			'CLE':'Cleveland Browns',
			'BUF':'Buffalo Bills',
			'BAL':'Baltimore Ravens',
			'KAN':'Kansas City Chiefs',
			'LAC':'Los Angeles Chargers',
			'SEA':'Seattle Seahawks',
			'DEN':'Denver Broncos',
			'WAS':'Washington Redskins',
			'ARI':'Arizona Cardinals',
			'DAL':'Dallas Cowboys',
			'CAR':'Carolina Panthers',
			'CHI':'Chicago Bears',
			'GNB':'Green Bay Packers',
			'NYJ':'New York Jets',
			'DET':'Detroit Lions',
			'LAR':'Los Angeles Rams',
			'STL':'St. Louis Rams',
			'OAK':'Oakland Raiders',
			'SDG':'San Diego Chargers'
		}
class TableColumns:
	def __init__(self):
		self.football_ref = {
		    'all_player_offense':[
				'player',
				'team',
				'pass_cmp',
				'pass_att',
				'pass_yds',
				'pass_td',
				'int',
				'sack',
				'sack_yds',
				'lng',
				'rate',
				'rush_att',
				'rush_yds',
				'rush_tds',
				'rush_lng',
				'rec_tgts',
				'rec',
				'rec_yds',
				'rec_tds',
				'rec_lng',
				'fmb',
				'fl'
		    ],
		    'all_targets_directions':[
			    'player',
				'team',
				'sl_tgt',
				'sl_rec',
				'sl_yds',
				'sl_tds',
				'sm_tgt',
				'sm_rec',
				'sm_yds',
				'sm_tds',
				'sr_tgt',
				'sr_rec',
				'sr_yds',
				'sr_tds',
				'dl_tgt',
				'dl_rec',
				'dl_yds',
				'dl_tds',
				'dm_tgt',
				'dm_rec',
				'dm_yds',
				'dm_tds',
				'dmr_tgt',
				'dmr_rec',
				'dmr_yds',
				'dmr_tds'
		    ],
		    'all_rush_directions':[
			    'player',
				'team',
				'le_att',
				'le_yds',
				'le_td',
				'lt_att',
				'lt_yds',
				'lt_td',
				'lg_att',
				'lg_yds',
				'lg_td',
				'm_att',
				'm_yds',
				'm_td',
				're_att',
				're_yds',
				're_td',
				'rt_att',
				'rt_yds',
				'rt_td',
				'rg_att',
				'rg_yds',
				'rg_td',
		    ],
		    'all_player_defense':[
		        'player',
				'team',
				'int',
				'int_yards',
				'int_td',
				'int_lng',
				'pd',
				'sacks',
				'tckl_comb',
				'tckl_solo',
				'tckl_ast',
				'tckl_for_loss',
				'qbhits',
				'fr',
				'fr_yds',
				'fr_tds',
				'ff'
		    ],
		    'all_returns':[
				'player',
				'team',
				'kor',
				'ko_yds',
				'ko_ypr',
				'ko_td',
				'ko_lng',
				'pr',
				'pr_yds',
				'pr_ypr',
				'pr_tds',
				'pr_lng'
		    ],
		    'all_home_snap_counts':[
				'player',
				'pos',
				'off_snaps',
				'off_pct',
				'def_snaps',
				'def_pct',
				'st_snaps',
				'st_pct'
		    ],
		    'all_vis_snap_counts':[
				'player',
				'pos',
				'off_snaps',
				'off_pct',
				'def_snaps',
				'def_pct',
				'st_snaps',
				'st_pct'
		    ]
		}
