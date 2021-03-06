from bs4 import BeautifulSoup as soup
from bs4 import Comment
from urllib.request import urlopen as uReq

class Scraper:

	def __init__(self,link):
		self.link = link
		self.page_soup = self.get_soup()

	# get soup object from link
	def get_soup(self):
		uClient = uReq(self.link)
		page_html = uClient.read()
		uClient.close()
		self.page_soup = soup(page_html, "lxml")
		return self.page_soup

	def get_link(self):
		return self.link

	def set_link(self,link):
		self.link = link
		self.page_soup = self.get_soup()
