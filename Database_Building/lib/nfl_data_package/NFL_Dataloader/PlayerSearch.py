import pandas as pd
import re
from scrapers import PFR_Gamepage

def update_table(table,temp_table):
    sql = "REPLACE INTO "+table
    sql += " (select * from "+temp_table+")"

def build_pfr_player_cache():
    ## get a collection of pfr links
    ## this will need to be a collection of unions for each position
    # select distinct (gs.gamelinks)
    #    from nfl_gamesummary gs, nfl_pbp pbp left join nfl_player_db pdb
    #    on pbp.playerid = pdb.playerid
    #    where pdb.playerid is null
    #    and nfl_pbp.gameid = nfl_gamesummary.gameid
    cols = ['playerid','player','team','pos']
    link = connection.execute(sql).fetchall().tolist()
    offense_cols_todrop = [
        'gameid',
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
    ]
    defense_cols_todrop = [
        'gameid',
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
    ]
    snapcount_cols_todrop = [
        'gameid',
        'player',
        'off_snaps',
        'off_pct',
        'def_snaps',
        'def_pct',
        'st_snaps',
        'st_pct'
    ]
    temp_df = pd.DataFrame(columns=cols,index=None)
    # **** needs testing **** #
    for link in links:
        pfr = PFR_Gamepage(link)

        # should return df with index playerid,player,team
        off_pfr_df = pfr.get_total_offense().set_index('playerid')
        off_pfr_df = off_pfr_df.drop(offense_cols_todrop,axis=1)
        def_pfr_df = pfr.get_defense().set_index('playerid')
        def_pfr_df = def_pfr_df.drop(defense_cols_todrop,axis=1)

        # should return df with index playerid, pos
        hsc_df = pfr.get_home_snapcounts().set_index('playerid')
        hsc_df = hsc_df.drop(snapcount_cols_todrop,axis=1)
        vsc_df = pfr.get_vis_snapcounts().set_index('playerid')
        vsc_df = hsc_df.drop(snapcount_cols_todrop,axis=1)

        df = off_pfr_df.join(def_pfr_df)
        df = df.join(hsc_df)
        df = df.join(vsc_df)
        temp_df = pd.concat([temp_df,df],axis=0,ignore_index=True)
        # returns a dataframe with playerid, player name, team, position

    temp_df.drop_duplicates(inplace=True,subset='playerid',keep='first')
    # store dataframe in database
    temp_df.to_sql('temp_pfr_cache',con='engine',if_exists='replace')

class PlayerSearch:
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
