from bs4 import BeautifulSoup
import requests

with open('simple.html') as html_file:
	soup = BeautifulSoup(html_file,'lxml')

# print(soup.prettify())
match = soup.title
print(match)
match = match.text
print(match)
match = soup.find('div', class_='footer')
print()
print(match)
