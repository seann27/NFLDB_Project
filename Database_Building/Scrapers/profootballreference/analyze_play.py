import re
import numpy as np
import pandas as pd
from references_dict import Team_Dictionary,DataFrameColumns

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
    "FG": re.compile("field goal (good|no good)")
}

class Play_Analysis:
    def __init__(self,play_list,player_dict):
        self.play_list = play_list
        self.player_dict = {}
        for key in player_dict:
            self.player_dict[key] = Player(player_dict[key])
        # for play in play list, update player dictionary

    def get_all_offense(self):
        # return summary passing/rushing/receiving stats
        print()

    def get_detailed_rushing(self):
        # return detailed rushing stats
        print()

    def get_detailed_receiving(self):
        # return detailed receiving stats
        print()

    def get_passing_stats(self):
        # return detailed receiving stats
        print()

class Player:
    def __init__(self,team):
        self.team = team

class Play:
    def __init__(self,play,player_dict):
        self.play = play
        self.play_type = ''
        self.play_components = []
        self.player_dict = player_dict

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
            # self.worksheet = 'PASS'
        elif key == 'RUN' or key == 'KNEEL' or key == 'SACK':
            self.play_type = 'RUSH'
            if key == 'RUN':
                self.play_components.append(search.group(1))
                self.play_components.append(search.group(2))
            if key == 'KNEEL' or key == 'SACK':
                self.play_components.append(key)
                self.play_components.append('')
            # self.worksheet = 'RUSH'
        elif key == 'YARDS':
            self.play_components.append(search.group(1))
        elif key == 'XP' or key == 'FG' or key == 'PUNT' or key == 'KICKOFF':
            if key == 'XP' or key == 'FG':
                self.play_components.append(search.group(1))
            # self.worksheet = 'ST'
        else:
            self.play_components.append(key)

    def analyze_components(self):
        print(*self.play_components, sep=',')
        # print("worksheet: "+self.worksheet)
        # self.write_metric(0,self.playnum)
        idx = 1
        for loop,comp in enumerate(self.play_components,0):
            if comp == 'TACKLE' or comp == 'INT' or comp == 'FUMBLE' or comp == 'PASS_DEF' or comp == 'SACK':
                # self.rownum[self.worksheet] += 1
                # type = self.worksheet
                # self.worksheet = 'DEF'
                # self.write_metric(0,self.playnum)
                # self.write_metric(1,type)
                idx = 2
                if comp == 'SACK':
                    row = self.rownum['RUSH']-1
                    self.worksheets['RUSH'].write(row,2,'SACK')
                    self.worksheets['RUSH'].write(row,4,self.play_components[loop+3])
                    del self.play_components[loop+3]
                    del self.play_components[loop+1]
            if comp == 'RETURN' and self.worksheet == 'DEF':
                idx +=1
                continue
            if comp == 'PENALTY':
                self.rownum[self.worksheet] += 1
                self.worksheet = 'PENALTY'
                self.write_metric(0,self.playnum)
                idx = 1
            if comp == 'NO GAIN': comp = '0'
            self.write_metric(idx,comp)
            idx += 1

    def write_misc(self):
        self.write_metric(0,self.playnum)
        self.write_metric(1,self.play.text)

    def analyze_play(self):
        play = self.play.text
        atags = self.play.findAll('a')
        atags.pop(0)
        playstring = ''
        for tag in atags:
            playstring = playstring+tag['href']
            if(tag.next_sibling):
                playstring += tag.next_sibling
        print(play)
        if len(playstring) == 0:
            playstring = play
        if play.startswith('Penalty on '):
            playstring = 'Penalty on '+playstring
        # print(playstring)
        keywords = playstring.split()
        wordbank = ''

        for word in keywords:
            wordbank += word+' '
            metric = self.process_word(wordbank)
            if metric:
                wordbank = ''
        if self.play_type == 'PASS' or self.play_type == 'RUSH':
            self.player_dict = self.analyze_components()

        return self.player_dict
