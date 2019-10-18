from .GeneralScraper import Scraper
from NFL_RefMaps import TableColumns
from bs4 import BeautifulSoup as soup
from bs4 import Comment
import pandas as pd
import numpy as np

class PFR_PlayerId_Mapper:

	def __init__(self,nfl_api_playerid):
		self.nflapi_player = nfl_api_playerid

		


		Scraper.__init__(self,link)
