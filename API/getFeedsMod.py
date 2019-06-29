from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import sys,traceback
import requests
import json
import time
from lxml import etree
while True:
    client = MongoClient('localhost:27017',username='root',password='ATIhH2s9gqpc')
    db = client.admin
    collection = db.News
    #import xml.etree.ElementTree as ET
    newsObj = {"news":[]}
    #{"status": "ok", "articles":[]}
    #namespaces = {'media':'http://search.yahoo.com/mrss/'}
    mainData = {"status": "ok","articles":[]}
    try:
        response = requests.get('http://feeds.bbci.co.uk/news/world/rss.xml')
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:BBC)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            image = ""
            data['urlToImage'] = "./img/BBCLogo.jpg"
            '''
            mediaGroup = newsItem.find('media:thumbnail',newsItem.nsmap)
            if mediaGroup is not None:
                for m in mediaGroup:
                    image = m.attrib['url']
                    data['urlToImage'] = image
                    break
                if image is "":
                    data['urlToImage'] = "./img/BBCLogo.jpg"
            '''
            mainData['articles'].append(data)
    except:
        print "Error in Int bbc",sys.exc_info()
        #print (newsItem.findall('media:thumbnail',namespaces))
    try:
        response = requests.get('https://feeds.a.dj.com/rss/RSSWorldNews.xml')
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:WSJ)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = "./img/wall-street-journal.png"
            mainData['articles'].append(data)
    except:
        print "Error in wsj-world"
    try:
        response = requests.get('https://www.news18.com/rss/world.xml')
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            desc = newsItem.find('description').text
            data['title'] = newsItem.find('title').text+'(source:News18)'
            start = desc.index('=')+2
            data['urlToImage'] =  desc[start:desc.index('\'',start)]
            data['url'] = newsItem.find('guid').text
            desc_start = desc.index('>')+1
            data['description'] = desc[desc_start:]
            mainData['articles'].append(data)
    except:
        print "Error in news18-world",sys.exc_info()       
    try:
        response = requests.get('http://rss.cnn.com/rss/edition_world.rss')
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:CNN)'
            desc = newsItem.find('description').text
            if "<" in desc:
                temp_desc = desc[0:desc.index('<')]
                data['description'] = temp_desc
            else:
                data['description'] = desc
            data['url'] = newsItem.find('link').text
        #data['urlToImage'] = newsItem.find('media:group',newsItem.nsmap)
        #data['publishedAt'] = newsItem.find('pubDate')
            img = ""
            mediaGroup = newsItem.find('media:group',newsItem.nsmap)
            if mediaGroup is not None:
                for m in mediaGroup:
                    img = m.attrib['url']
                    data['urlToImage'] = img
                    break
            if img is "":
                data['urlToImage'] = "./img/cnnLogo.png"
            mainData['articles'].append(data)
    except:
        print "Error in Int cnn",sys.exc_info()[0]
    try:
    	response = requests.get('http://feeds.feedburner.com/ndtvnews-world-news')
    	root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:NDTV)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('fullimage').text
            mainData['articles'].append(data)
    except:
        print "Error in ndtv"
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "world done"
    #general
    try:
    	response = requests.get('http://feeds.feedburner.com/ndtvnews-india-news')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:NDTV)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('fullimage').text
            mainData['articles'].append(data)
    except:
        print "Error in ndtv-India"
    
    try:
        response = requests.get('https://zeenews.india.com/rss/india-national-news.xml')
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data ={}
            data['title'] = newsItem.find('title').text+'(source:ZeeNews)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = './img/zeeNews.jpg'
            mainData['articles'].append(data)
    except:
        print 'Error in ZeeNews'
    try:
    	response = requests.get('https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms')
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
            imageUrl = newsItem.find('link').text
            initialUrl = "https://timesofindia.indiatimes.com"
            page = requests.get(imageUrl)
            soup = BeautifulSoup(page.content, 'lxml')
            html = list(soup.children)[1]
            l = soup.find_all('section', class_='highlight clearfix')
            if len(l)>0:
                content=str(l[0])
                src_index = content.index("/thumb")
                jpg_index = content.index("jpg",src_index)
                data['urlToImage'] = initialUrl + content[src_index:jpg_index] + "jpg"
                mainData['articles'].append(data)
    except:
        print "Error in toi"
    try:
        response = requests.get('https://www.thehindu.com/news/national/feeder/default.rss')
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data ={}
            data['title'] = newsItem.find('title').text+'(source:TheHindu)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = './img/theHindu.jpg'
            mainData['articles'].append(data)
    except:
        print 'Error in TheHindu'
    try:
    	response = requests.get('https://www.hindustantimes.com/rss/india/rssfeed.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:HT)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in HT"
 
    try:
    	response = requests.get('https://www.firstpost.com/rss/india.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:FP)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
            if "dummy" in data['urlToImage']:
                data['urlToImage'] = "./img/firstpostLogo.jpg"
            mainData['articles'].append(data)
    except:
        print "Error in fp"

    print "General Done" 
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    #Business
    try:
    	response = requests.get('https://www.firstpost.com/rss/business.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:FP)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
            if "dummy" in data['urlToImage']:
                data['urlToImage'] = "./img/firstpostLogo.jpg"
            mainData['articles'].append(data)
    except:
        print "Error in fp-business"

    try:
    	response = requests.get('http://feeds.feedburner.com/ndtvprofit-latest')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:NDTV)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('fullimage').text
            mainData['articles'].append(data)
    except:
        print "Error in ndtv-profit"
    try:
    	response = requests.get('https://www.hindustantimes.com/rss/business/rssfeed.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:HT)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in ht-business"
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Business Done"
    #Entertainment
    try:
    	response = requests.get('http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:BBC)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = "./img/BBCLogo.jpg"
            #newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
        #print (newsItem.findall('media:thumbnail',namespaces))
    except:
        print "Error in bbc-ent"
    try:
    	response = requests.get('https://www.hindustantimes.com/rss/entertainment/rssfeed.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:HT)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in ht-ent"
    ''' 
    response = requests.get('https://www.firstpost.com/rss/bollywood.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        try:
            data = {}
            data['title'] = newsItem.find('title').text
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
            if "dummy" in data['urlToImage']:
                data['urlToImage'] = "./img/firstpostLogo.jpg"
            mainData['articles'].append(data)
        except:
            print "Error in fp-ent"
    '''
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Ent Done"
    #Health
    try:
    	response = requests.get('http://feeds.feedburner.com/ndtvcooks-latest')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:NDTV)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('fullimage').text
            mainData['articles'].append(data)
    except:
        print "Error in ndtv-cooks"
    try:
    	response = requests.get('https://www.hindustantimes.com/rss/health-fitness/rssfeed.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:HT)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in ht-health"

    try:
    	response = requests.get('http://feeds.bbci.co.uk/news/health/rss.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:BBC)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = "./img/BBCLogo.jpg"
            #newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
        #print (newsItem.findall('media:thumbnail',namespaces))
    except:
        print "Error in bbc-health"

    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Health Done"
    #science
    try:
    	response = requests.get('http://feeds.bbci.co.uk/news/science_and_environment/rss.xml')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
	    data['title'] = newsItem.find('title').text+'(source:BBC)'
	    data['description'] = newsItem.find('description').text
      	    data['url'] = newsItem.find('link').text
	    data['publishedAt'] = newsItem.find('pubDate').text
	    data['urlToImage'] = "./img/BBCLogo.jpg"
            #newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in bbc-science"

    try:
    	response = requests.get('https://indianexpress.com/section/technology/feed/')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:IEx)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in iex-science"
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Science Done"
    #sports
#    try:
 #   	response = requests.get('https://www.hindustantimes.com/rss/sports/rssfeed.xml')
  #  	root = etree.fromstring(response.content)
   # 	for newsItem in root.iter('item'):
    #        data = {}
     #       data['title'] = newsItem.find('title').text+'(source:HT)'
      #      data['description'] =  newsItem.find('description').text
       #     data['url'] = newsItem.find('link').text
        #    data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
         #   mainData['articles'].append(data)
   # except:
    #    print "Error in ht-sports"

    try:
    	response = requests.get('http://feeds.feedburner.com/ndtvsports-latest')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:NDTV)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('fullimage').text
            mainData['articles'].append(data)
    except:
        print "Error in ndtv-sports"
    try:
    	response = requests.get('https://indianexpress.com/section/sports/feed/')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:IEx)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in iex-sports",sys.exc_info()
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Sports Done"
    #Technology
    try:
    	response = requests.get('https://www.techradar.com/rss')
    	root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:TechRadar)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = newsItem.find('enclosure',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in TechRadar",sys.exc_info()[0]

    try:
    	response = requests.get('http://feeds.bbci.co.uk/news/technology/rss.xml')
    	root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:BBC)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = "./img/BBCLogo.jpg"
            #newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in Tech",sys.exc_info()[0]
    try:
    	response = requests.get('http://feeds.feedburner.com/gadgets360-latest')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:Gadgets360)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('fullimage').text
            mainData['articles'].append(data)
    except:
        print "Error in gadgets-360"
    try:
    	response = requests.get('https://feeds.a.dj.com/rss/RSSWSJD.xml')
    	root = etree.fromstring(response.content)
        logo = None
        for imgItem in root.iter('image'):
            logo = imgItem.find('url').text
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:WSJ)'
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = "./img/wall-street-journal.png"
            mainData['articles'].append(data)
    except:
        print "Error in wsj-tech"
    '''
    response = requests.get('https://www.techradar.com/rss')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        try:
            data = {}
            data['title'] = newsItem.find('title').text
            data['description'] =  newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['urlToImage'] = newsItem.find('enclosure').attrib['url']
            mainData['articles'].append(data)
        except:
            print "Error in techradar"
    '''
    try:
    	response = requests.get('http://feeds.feedburner.com/TechCrunch/')
    	root = etree.fromstring(response.content)
    	for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:TechCrunch)'
            tc_desc = newsItem.find('description').text
            temp = re.sub("&#8230;","...",tc_desc)
            temp = re.sub("&#8217;","'",temp)
            temp = re.sub("&#8220;","\"",temp)
            temp = re.sub("&#8221;","\"",temp)
            temp = re.sub("&#8212;","-",temp)
            data['description'] = temp
            data['url'] = newsItem.find('link').text
            content = newsItem.find('content:encoded',newsItem.nsmap).text
            initial = content.index("src")
            #temp = content[initial:content.index("alt",initial)]
            #imgUrl = temp[temp.index("http"):len(temp)-2]
            #data['urlToImage'] = imgUrl
            imageUrl = data['url']
            page = requests.get(imageUrl)
            soup = BeautifulSoup(page.content, 'lxml')
            html = list(soup.children)[1]
            l = soup.find_all('img', class_='article__featured-image')
            if len(l)>0:
                content=str(l[0])
                src_index = content.index("https")
                #print(content[src_index:len(content)-3])
                data['urlToImage'] = content[src_index:len(content)-3]
            mainData['articles'].append(data)
    except:
        print "Error in TechCrunch"
    
    newsObj['news'].append(mainData)
    print "Tech Done"
    mainData = {"status": "ok","articles":[]}
    #Current Affairs
    try:
    	response = requests.get('https://www.jagranjosh.com/rss/josh/current_affairs.xml')
    	root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:JagranJosh)'
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = "./img/jagranLogo.png"
            mainData['articles'].append(data)
    except:
        print "Error in JagranJosh",sys.exc_info()[0]
    
    newsObj['news'].append(mainData)
    print "Current Affairs Done"
    mainData = {"status": "ok", "articles":[]}
    try:
        response = requests.get('http://feeds.feedburner.com/ndtvnews-offbeat-news')
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:NDTV)'
            data['description'] = newsItem.find('description').text
            data['urlToImage'] = newsItem.find('fullimage').text
            data['url'] = newsItem.find('link').text
            mainData['articles'].append(data)
    except:
        print 'Error in NDTV Offbeat'
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get('https://www.sciencedaily.com/rss/strange_offbeat.xml',headers=headers)
        root = etree.fromstring(response.content)
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text+'(source:ScienceDaily)'
            data['description'] = newsItem.find('description').text
            image = newsItem.find('media:thumbnail',newsItem.nsmap)
            if image is not None:
                data['urlToImage'] = image.attrib['url']
            else:
                data['urlToImage'] = './img/scienceDaily.png'
#            data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            data['url'] = newsItem.find('link').text
            mainData['articles'].append(data)
    except:
        print 'Error in ScienceDaily',sys.exc_info()   
    
    newsObj['news'].append(mainData)
    print 'Offbeat done'
    #json_data = json.dumps(newsObj)
    rec_id = collection.insert_one(newsObj)
    print("Data Inserted with record id",rec_id)
    #print json_data
    time.sleep(300)
