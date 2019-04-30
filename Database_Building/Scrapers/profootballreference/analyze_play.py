import re
import numpy as np
import pandas as pd
import analyze_play
from references_dict import Team_Dictionary,DataFrameColumns,WebsiteBugs

regex = {
	"PLAYER": re.compile("/players/.*\.htm"),
	"PASS": re.compile("pass (complete|incomplete) (short|deep) (right|left|middle)"),
	"RUN": re.compile("(up the|right|left) (guard|end|tackle|middle)"),
	"YARDS": re.compile("([-]?\d+) yard"),
	"NO GAIN": re.compile("no gain"),
	"TACKLE": re.compile("tackle by"),
	"TD": re.compile("touchdown"),
	"TB": re.compile("touchback"),
	"SACK": re.compile("sacked by"),
	"PASS_DEF": re.compile("defended by"),
	"FUMBLE": re.compile("fumbles"),
	"RECOVERED": re.compile("recovered by"),
	"KICKOFF": re.compile("kicks off"),
	"RETURN": re.compile("returned"),
	"INT": re.compile("intercepted by"),
	"TIMEOUT": re.compile("Timeout #(\d)"),
	"CHALL": re.compile("challenged"),
	"XP": re.compile("kicks extra point (good|no good)"),
	"PUNT": re.compile("punts"),
	"OOB": re.compile("out of bounds"),
	"FC": re.compile("fair catch by"),
	"KNEEL": re.compile("kneels"),
	"PENALTY": re.compile("Penalty on"),
	"FG": re.compile("field goal (good|no good)"),
	"NO_PLAY": re.compile("no play"),
	"TWO_POINT_ATTEMPT": re.compile("Two Point Attempt")
}

class Play_Analysis:
	def __init__(self,play_list,player_dict):
		self.play_list = play_list
		self.player_dict = player_dict
		# for play in play list, update player dictionary
		self.analyze_all_plays()

	def analyze_all_plays(self):
		for play in self.play_list:
			pa = Play(play,self.player_dict)
			self.player_dict = pa.player_dict

	def filter_players(self):
		tmp_dict = {}
		for key,player in self.player_dict.items():
			stat_check = 0
			stat_check += player.rushatt
			stat_check += player.rushyds
			stat_check += player.rushtds
			stat_check += player.recatt
			stat_check += player.rec
			stat_check += player.recyds
			stat_check += player.rectds
			stat_check += player.fmb
			stat_check += player.passatt
			stat_check += player.passcomp
			stat_check += player.passyds
			stat_check += player.passtds
			stat_check += player.int
			stat_check += player.sacked
			stat_check += player.sacked_yds
			stat_check += player.rtn_tds
			if stat_check > 0:
				player.summarize_offense()
				tmp_dict[key] = player
		self.player_dict = tmp_dict

	def filter_rushing_players(self):
		tmp_dict = {}
		locations = ('end','guard','tackle')
		metrics = ('att','yds','tds')
		for key,player in self.player_dict.items():
			stat_check = 0
			for l in locations:
				for m in metrics:
					stat_check += player.rushing['left'][l][m]
			for m in metrics:
				stat_check += player.rushing['upthe']['middle'][m]
			for l in locations:
				for m in metrics:
					stat_check += player.rushing['right'][l][m]
			if stat_check > 0:
				player.summarize_rushing()
				tmp_dict[key] = player
		return tmp_dict

	def filter_receiving_players(self):
		tmp_dict = {}
		depths = ('short','deep')
		directions = ('left','middle','right')
		metrics = ('att','catches','yds','tds')
		for key,player in self.player_dict.items():
			stat_check = 0
			for d in depths:
				for r in directions:
					for m in metrics:
						stat_check += player.receiving[d][r][m]
			if stat_check > 0:
				player.summarize_receiving()
				tmp_dict[key] = player
		return tmp_dict

	def get_all_offense(self):
		metric_list = []
		columns = DataFrameColumns().football_ref['PBP_ALL_OFF']
		player_dict = self.filter_players()
		for key,val in sorted (self.player_dict.items()):
			metric_list.append(val.all_off_metrics)
		metric_list = np.asarray(metric_list)
		df = pd.DataFrame(metric_list,columns=columns)
		return df

	def get_detailed_rushing(self):
		metric_list = []
		columns = DataFrameColumns().football_ref['RUSH']
		player_dict = self.filter_rushing_players()
		for key,val in sorted (player_dict.items()):
			metric_list.append(val.detailed_rush_metrics)
		metric_list = np.asarray(metric_list)
		df = pd.DataFrame(metric_list,columns=columns)
		return df

	def get_detailed_receiving(self):
		metric_list = []
		columns = DataFrameColumns().football_ref['REC']
		player_dict = self.filter_receiving_players()
		for key,val in sorted (player_dict.items()):
				metric_list.append(val.detailed_rec_metrics)
		metric_list = np.asarray(metric_list)
		df = pd.DataFrame(metric_list,columns=columns)
		return df

class Play:
	def __init__(self,play,player_dict):
		self.play = play
		self.play_type = ''
		self.interception = 0
		self.fumble = 0
		self.fumble_player_idx = 0
		self.play_components = []
		self.player_components = []
		self.player_dict = player_dict
		self.player_dict = self.analyze_play()

	def process_word(self,word):
		match = ''
		for key in regex:
			search = regex[key].search(word)
			if search:
				self.process_match(key,search)
				match = key
		return match

	def process_match(self,key,search):
		if key == 'PLAYER':
			self.play_components.append(search.group(0))
		elif key == 'PASS':
			self.play_type = 'PASS'
			self.play_components.append(search.group(1))
			self.play_components.append(search.group(2))
			self.play_components.append(search.group(3))
		elif key == 'RUN' or key == 'KNEEL':
			self.play_type = 'RUSH'
			if key == 'RUN':
				self.play_components.append(search.group(1))
				self.play_components.append(search.group(2))
			if key == 'KNEEL':
				self.play_components.append("up the")
				self.play_components.append('middle')
		elif key == 'SACK':
			self.play_type = 'SACK'
		elif key == 'YARDS':
			self.play_components.append(search.group(1))
		elif key == 'NO GAIN':
			self.play_components.append('0')
		elif key == 'INT':
			self.interception = 1
		elif key == 'RECOVERED':
			self.fumble_player_idx = len(self.play_components)
		elif key == 'XP' or key == 'FG' or key == 'PUNT' or key == 'KICKOFF':
			if key == 'XP' or key == 'FG':
				self.play_components.append(search.group(1))
		elif key == 'NO_PLAY':
			self.play_type = 'NO PLAY'
		else:
			self.play_components.append(key)

	def analyze_components(self):
		# print(*self.play_components, sep=',')
		comps = self.play_components
		player1 = comps[0]
		player1 = self.player_dict[player1]
		idx = 1
		if self.fumble_player_idx > 0:
			recovering_player = comps[self.fumble_player_idx]
			if player1.team != self.player_dict[recovering_player].team:
				self.fumble = 1

		if self.play_type == 'PASS':
			player2 = comps[4]
			if player2 in WebsiteBugs().football_ref.keys():
				player2 = WebsiteBugs().football_ref[player2]
			player2 = self.player_dict[player2]
			player1.passatt += 1
			player2.recatt += 1
			player2.receiving[comps[2]][comps[3]]['att'] += 1
			if self.interception == 1:
				player1.int += 1
			elif self.fumble == 1:
				player2.fmb += 1
			else:
				if comps[1] == 'complete':
					player1.passcomp += 1
					player1.passyds += int(comps[5])
					player2.rec += 1
					player2.receiving[comps[2]][comps[3]]['catches'] += 1
					player2.recyds += int(comps[5])
					player2.receiving[comps[2]][comps[3]]['yds'] += int(comps[5])
					if len(comps) > 6:
						if comps[6] == 'TD':
							player1.passtds += 1
							player2.rectds += 1
							player2.receiving[comps[2]][comps[3]]['tds'] += 1

		if self.play_type == 'RUSH':
			comps[1] = comps[1].replace(" ","")
			player1.rushatt += 1
			player1.rushing[comps[1]][comps[2]]['att'] += 1
			if self.fumble == 1:
				player1.fmb += 1
			else:
				if regex['TWO_POINT_ATTEMPT'].search(self.play.text):
					player1.rushyds += 2
					player1.rushing[comps[1]][comps[2]]['yds'] += 2
				else:
					player1.rushyds += int(comps[3])
					player1.rushing[comps[1]][comps[2]]['yds'] += int(comps[3])
				if len(comps) > 4:
					if comps[4] == 'TD':
						player1.rushtds += 1
						player1.rushing[comps[1]][comps[2]]['tds'] += 1

		if self.play_type == 'SACK':
			player1.sacked += 1
			yd_idx = 2
			if regex['PLAYER'].search(comps[yd_idx]):
				yd_idx += 1
			player1.sacked_yds += int(yd_idx)
			if self.fumble == 1:
				player1.fmb += 1

	def analyze_play(self):
		play = self.play.text
		atags = self.play.findAll('a')
		if len(atags) == 0:
			return self.player_dict
		atags.pop(0)
		playstring = ''
		for tag in atags:
			playstring = playstring+tag['href']
			if(tag.next_sibling):
				playstring += tag.next_sibling
		if len(playstring) == 0:
			playstring = play
		if play.startswith('Penalty on '):
			playstring = 'Penalty on '+playstring
		keywords = playstring.split()
		wordbank = ''

		for word in keywords:
			wordbank += word+' '
			metric = self.process_word(wordbank)
			if metric:
				wordbank = ''
		if self.play_type == 'PASS' or self.play_type == 'RUSH' or self.play_type == 'SACK':
			self.analyze_components()

		return self.player_dict
