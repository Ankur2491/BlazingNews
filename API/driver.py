from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import sys,traceback
import requests
import json
import time
from lxml import etree
mainData = {}
try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get('https://www.techradar.com/rss',headers=headers)
        print response
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:TOI)'
            description = newsItem.find('description').text
            if description:
                if "</a>" in description:
                    desc = newsItem.find('description').text.split("</a>")
                    data['description'] = desc[1]
                else:
                    data['description'] = description
            data['url'] = newsItem.find('link').text
            imageUrl = 'https://zeenews.india.com/india/sc-to-hear-plea-for-early-hearing-of-ayodhya-land-dispute-case-on-thursday-2218344.html'
            initialUrl = "https://timesofindia.indiatimes.com"
            page = requests.get(imageUrl)
            soup = BeautifulSoup(page.content, 'lxml')
            html = list(soup.children)[1]
            l = soup.find_all('div', class_='article-image-block')
            if len(l)>0:
                content=str(l[0])
                src_index = content.index("src=")+5
                jpg_index = content.index("\"",src_index)
                print content[src_index:jpg_index]
except:
        print "Error in toi",sys.exc_info()
