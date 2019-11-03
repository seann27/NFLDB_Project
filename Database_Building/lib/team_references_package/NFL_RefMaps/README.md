# NFL_RefMaps

Summary

# Files
TeamAbbrev.py - Class that maps team abbreviations/names for specific websites
TableColumns.py - Class that maps column names for scraped tables
DFColumns.py - Class that maps DataFrame templating information
WebsiteBugs.py - Class that maps broken links on websites for scraping


# installation

pip install --upgrade NFL_RefMaps

# TeamAbbrev usage

- website specific maps are stored as object attributes

	>>> from NFL_RefMaps import TeamDictionary
	>>> kaggle_team_names = TeamDictionary().kaggle_abbrev
    >>> team_abbrev = kaggle_team_names['Denver Broncos']
    >>> team_abbrev
    Out: 'DEN'

- to get the inverse of a dictionary, call the get_reverse_dict class method

    >>> team_dict = TeamDictionary()
    >>> kaggle_team_abbrev = team_dict.get_reverse_dict(team_dict.kaggle_abbrev)
    >>> team_name = kaggle_team_abbrev['DEN']
    >>> team_name
    Out: 'Denver Broncos'

# TableColumns usage

- dictionaries with table names are stored as object attributes per website
- table names are dictionaries that map to lists

    >>> from NFL_RefMaps import TableColumns
    >>> pfr_tables = TableColumns().football_ref
    >>> all_offense_cols = pfr_tables['all_player_offense']
    >>> all_offense_df = pd.DataFrame(columns=all_offense_cols)
