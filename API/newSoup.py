import requests
from bs4 import BeautifulSoup
page = requests.get("https://timesofindia.indiatimes.com/city/delhi/Green-court-bans-vehicles-older-than-15-years-in-Delhi/articleshow/45290291.cms")
#print page.content
soup = BeautifulSoup(page.content, 'html.parser')
html = list(soup.children)[1]
#print(len(list(html.children)))
l = soup.find_all('section', class_='highlight clearfix')
#print len(l)
content=str(l[0])
src_index = content.index("/thumb")
jpg_index = content.index("jpg",src_index)
print content[src_index:jpg_index]
