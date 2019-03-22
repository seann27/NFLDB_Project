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
    def __init__(self,play,workbook,worksheets):
        self.play = play
        self.workbook = workbook
        self.worksheets = worksheets
        self.play_components = []
        self.off_comp = []
        self.def_comp = []
        self.result = ''

    def process_match(self,key,search):
        if key == 'PLAYER':
            self.play_components.append(search.group(0))
        elif key == 'PASS':
            self.play_components.append(search.group(1))
            self.play_components.append(search.group(2))
            self.play_components.append(search.group(3))
        elif key == 'RUN':
            self.play_components.append(search.group(0))
            self.play_components.append(search.group(1))
        elif key == 'YARDS':
            self.play_components.append(search.group(1))
        elif key == 'XP' or key == 'FG':
            self.play_components.append(search.group(1))
        else:
            self.play_components.append(key)

    def search_word(self,word):
        match = ''
        for key in regex:
            search = regex[key].search(word)
            if search:
                print(word+"-"+key)
                self.process_match(key,search)
                match = key
        return match

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
            metric = self.search_word(wordbank)
            if metric:
                wordbank = ''
        print(*self.play_components, sep=',')
        print()
