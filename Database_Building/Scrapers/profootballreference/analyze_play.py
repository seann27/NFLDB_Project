import re
import xlsxwriter

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

class Metric:
    def __init__(self,metric,value):
        self.metric = metric
        self.value = value

class Play:
    def __init__(self,play,workbook,worksheets,playnum,rownum):
        self.play = play
        self.workbook = workbook
        self.worksheets = worksheets
        self.worksheet = 'MISC'
        self.playnum = playnum
        self.rownum = rownum
        self.play_components = []
        self.players = []
        self.result = ''

    def process_word(self,word):
        match = ''
        for key in regex:
            search = regex[key].search(word)
            if search:
                # print(word+"-"+key)
                self.process_match(key,search)
                match = key
        return match

    def process_match(self,key,search):
        if key == 'PLAYER':
            self.play_components.append(search.group(0))
        elif key == 'PASS':
            self.play_components.append(search.group(1))
            self.play_components.append(search.group(2))
            self.play_components.append(search.group(3))
            self.worksheet = 'PASS'
        elif key == 'RUN' or key == 'KNEEL' or key == 'SACK':
            if key == 'RUN':
                self.play_components.append(search.group(1))
                self.play_components.append(search.group(2))
            if key == 'KNEEL' or key == 'SACK':
                self.play_components.append(key)
                self.play_components.append('')
            self.worksheet = 'RUSH'
        elif key == 'YARDS':
            self.play_components.append(search.group(1))
        elif key == 'XP' or key == 'FG' or key == 'PUNT' or key == 'KICKOFF':
            if key == 'XP' or key == 'FG':
                self.play_components.append(search.group(1))
            self.worksheet = 'ST'
        else:
            self.play_components.append(key)

    def write_metric(self,col,value):
        row = self.rownum[self.worksheet]
        self.worksheets[self.worksheet].write(row,col,value)

    def write_components(self):
        print(*self.play_components, sep=',')
        print("worksheet: "+self.worksheet)
        self.write_metric(0,self.playnum)
        idx = 1
        for loop,comp in enumerate(self.play_components,0):
            if comp == 'TACKLE' or comp == 'INT' or comp == 'FUMBLE' or comp == 'PASS_DEF' or comp == 'SACK':
                self.rownum[self.worksheet] += 1
                type = self.worksheet
                self.worksheet = 'DEF'
                self.write_metric(0,self.playnum)
                self.write_metric(1,type)
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
        if self.worksheet != 'MISC':
            self.write_components()
        else:
            self.write_misc()
        print()
        self.rownum[self.worksheet] += 1
