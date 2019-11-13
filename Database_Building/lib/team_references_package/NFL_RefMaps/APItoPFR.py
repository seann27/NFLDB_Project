import pandas as pd
import re
from scrapers import PFR_Gamepage

class MapPlayer:
    '''
    Required Args:
    * api_id - player id provided by the NFL API
    * api_name - player name provided by the NFL API
    * links - list of pro-football-reference links where player could be
              extracted from
    '''
    def __init__(self,api_id,api_name,team,links):

        api_name = api_name.split('.')
        self.api_id = api_id
        self.api_first_initial = api_name[0]
        self.api_last_name = api_name[1]
        self.team = team
        self.links = links

    '''
    Returns:
        player link, player name, position, game link
    '''
    def search_player(self):
        found = 0
        cross_check = 0
        player_id = ''
        player_name = ''
        plyr_pos = ''
        final_link = ''
        positions = [
            'QB',
            'RB',
            'WR',
            'TE'
        ]
        for link in self.links:
            pfr = PFR_Gamepage(link)
            pfr_df = pfr.get_total_offense()
            names = pfr_df['player'].tolist()
            ids = pfr_df['playerid'].tolist()
            teams = pfr_df['team'].tolist()

            # first check their name for total offense
            for idx,name in enumerate(names):
                search = '^'+self.api_first_initial+'.*'+self.last_name
                search = re.search(search,name)
                if search:
                    if self.team == teams[idx]:
                        found += 1
                        player_name = name
                        player_id = ids[idx]

            # cross reference with the snapcounts
            hsc = get_home_snapcounts()
            vsc = get_vis_snapcounts()
            pos = hsc['pos'].tolist()+vsc['pos'].tolist()
            snapcounts = hsc['playerid'].tolist()+vsc['playerid'].tolist()
            for idx,pid in enumerate(snapcounts):
                if playerid == pid:
                    if pos[idx] in positions:
                        plyr_pos = pos[idx]
                        cross_check += 1

            if found > 0:
                return player_id,player_name,plyr_pos,link

        print("Matches found: "+str(found))
        print("Passed cross check: "+str(cross_check))
        if found == 0:
            print("Warning, no matches for that player found!")
