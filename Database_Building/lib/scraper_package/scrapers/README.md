# Web scraping package for sports stats

Summary

# Files
PFRScraper.py - Class that scrapes tables from pro-football-reference.com
    - PFR_Gamelinks, PFR_Gamepage
GeneralScraper.py - Parent class that connects, scrapes, and returns soup object

# PFR_Gamelinks object arguments
1) season
2) week

# PFR_Gamepage object arguments
1) link

# Usage
    >>> gamelinks = PFR_Gamelinks(2019,6)
    >>> game1 = gamelinks[0]
    
    >>> game1_pfrs = PFR_Gamepage(game1)
    >>> game1_gameinfo = game1_pfrs.get_gameinfo

# installation

pip install --upgrade scrapers
