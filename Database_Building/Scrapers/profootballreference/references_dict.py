class Team_Dictionary:
	def __init__(self):
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

class DataFrameColumns:
	def __init__(self):
		self.football_ref = {
		    'GAMEINFO':[
		        'GameID',
		        'Season',
		        'Week',
		        'HomeTeamID',
		        'HomePoints',
		        'AwayTeamID',
		        'AwayPoints',
		        'VegasLine',
		        'O/U'
		    ],
		    'SNAPCOUNTS':[
		        'GameID',
		        'PlayerID',
		        'Name',
		        'Position',
		        'Team',
		        'Snapcount',
		        'Snapcount_PCT'
		    ],
			'ALL_OFF':[
				'GAMEID',
				'PLAYER',
				'TEAM',
				'PASS_CMP',
				'PASS_ATT',
				'PASS_YDS',
				'PASS_TD',
				'PASS_INT',
				'PASS_SK',
				'PASS_SK_YDS',
				'PASS_LNG',
				'PASS_RATE',
				'RUSH_ATT',
				'RUSH_YDS',
				'RUSH_TD',
				'RUSH_LNG',
				'REC_TGT',
				'REC_REC',
				'REC_YDS',
				'REC_TD',
				'REC_LNG',
				'FMB',
				'FL'
			],
			'PBP_ALL_OFF':[
				'GAMEID',
				'PLAYER',
				'TEAM',
				'PASS_CMP',
				'PASS_ATT',
				'PASS_YDS',
				'PASS_TD',
				'PASS_INT',
				'PASS_SK',
				'PASS_SK_YDS',
				'RUSH_ATT',
				'RUSH_YDS',
				'RUSH_TD',
				'REC_TGT',
				'REC_REC',
				'REC_YDS',
				'REC_TD',
				'FL'
			],
		    'REC':[
				'GAMEID',
				'PLAYER',
				'TEAM',
		        'SL_TGT',
		        'SL_CATCH',
		        'SL_YDS',
		        'SL_TD',
		        'SM_TGT',
		        'SM_CATCH',
		        'SM_YDS',
		        'SM_TD',
		        'SR_TGT',
		        'SR_CATCH',
		        'SR_YDS',
		        'SR_TD',
		        'DL_TGT',
		        'DL_CATCH',
		        'DL_YDS',
		        'DL_TD',
		        'DM_TGT',
		        'DM_CATCH',
		        'DM_YDS',
		        'DM_TD',
		        'DR_TGT',
		        'DR_CATCH',
		        'DR_YDS',
		        'DR_TD',
		    ],
		    'RUSH':[
				'GAMEID',
				'PLAYER',
				'TEAM',
		        'LE_ATT',
		        'LE_YDS',
		        'LE_TD',
		        'LT_ATT',
		        'LT_YDS',
		        'LT_TD',
		        'LG_ATT',
		        'LG_YDS',
		        'LG_TD',
		        'M_ATT',
		        'M_YDS',
		        'M_TD',
		        'RE_ATT',
		        'RE_YDS',
		        'RE_TD',
		        'RT_ATT',
		        'RT_YDS',
		        'RT_TD',
		        'RG_ATT',
		        'RG_YDS',
		        'RG_TD',
		    ],
			'DST':[
				'GAMEID',
				'TEAM',
				'SACKS',
				'INT',
				'FR',
				'TDS',
				'TWOPT',
				'BLOCK'
			]
		}
