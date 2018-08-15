from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import sys
import requests
import json
import time
from lxml import etree
while True:
    client = MongoClient('localhost:27017')
    db = client.admin
    collection = db.News
    #import xml.etree.ElementTree as ET
    newsObj = {"news":[]}
    #{"status": "ok", "articles":[]}
    #namespaces = {'media':'http://search.yahoo.com/mrss/'}
    mainData = {"status": "ok","articles":[]}
    response = requests.get('http://feeds.bbci.co.uk/news/world/rss.xml')
    root = etree.fromstring(response.content)

    for newsItem in root.iter('item'):
        try:
            data = {}
            data['title'] = newsItem.find('title').text
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
        except:
            print "Error in Int bbc"
        #print (newsItem.findall('media:thumbnail',namespaces))

    response = requests.get('http://rss.cnn.com/rss/edition_world.rss')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        try:
            data = {}
            data['title'] = newsItem.find('title').text
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

    response = requests.get('http://feeds.feedburner.com/ndtvnews-world-news')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('fullimage').text
        mainData['articles'].append(data)

    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "world done"
    #general
    response = requests.get('http://feeds.feedburner.com/ndtvnews-india-news')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('fullimage').text
        mainData['articles'].append(data)

    response = requests.get('https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
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

    response = requests.get('https://www.hindustantimes.com/rss/india/rssfeed.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)

    response = requests.get('https://www.firstpost.com/rss/india.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        if "dummy" in data['urlToImage']:
            data['urlToImage'] = "./img/firstpostLogo.jpg"
        mainData['articles'].append(data)
    newsObj['news'].append(mainData)

    print "General Done"
    mainData = {"status": "ok","articles":[]}
    #Business
    response = requests.get('https://www.firstpost.com/rss/business.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        if "dummy" in data['urlToImage']:
            data['urlToImage'] = "./img/firstpostLogo.jpg"
        mainData['articles'].append(data)


    response = requests.get('http://feeds.feedburner.com/ndtvprofit-latest')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('fullimage').text
        mainData['articles'].append(data)

    response = requests.get('https://www.hindustantimes.com/rss/business/rssfeed.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Business Done"
    #Entertainment
    response = requests.get('http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] = newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['publishedAt'] = newsItem.find('pubDate').text
        data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)
        #print (newsItem.findall('media:thumbnail',namespaces))


    response = requests.get('https://www.hindustantimes.com/rss/entertainment/rssfeed.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)

    response = requests.get('https://www.firstpost.com/rss/bollywood.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        if "dummy" in data['urlToImage']:
            data['urlToImage'] = "./img/firstpostLogo.jpg"
        mainData['articles'].append(data)
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Ent Done"
    #Health
    response = requests.get('http://feeds.feedburner.com/ndtvcooks-latest')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('fullimage').text
        mainData['articles'].append(data)


    response = requests.get('https://www.hindustantimes.com/rss/health-fitness/rssfeed.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)

    response = requests.get('http://feeds.bbci.co.uk/news/health/rss.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] = newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['publishedAt'] = newsItem.find('pubDate').text
        data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)
        #print (newsItem.findall('media:thumbnail',namespaces))
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Health Done"
    #science

    response = requests.get('http://feeds.bbci.co.uk/news/science_and_environment/rss.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] = newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['publishedAt'] = newsItem.find('pubDate').text
        data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)



    response = requests.get('https://indianexpress.com/section/technology/feed/')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] = newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['publishedAt'] = newsItem.find('pubDate').text
        data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Science Done"
    #sports
    response = requests.get('https://www.hindustantimes.com/rss/sports/rssfeed.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)


    response = requests.get('http://feeds.feedburner.com/ndtvsports-latest')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('fullimage').text
        mainData['articles'].append(data)

    response = requests.get('https://indianexpress.com/section/sports/feed/')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] = newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['publishedAt'] = newsItem.find('pubDate').text
        data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)
    newsObj['news'].append(mainData)
    mainData = {"status": "ok","articles":[]}
    print "Sports Done"
    #Technology

    response = requests.get('http://feeds.bbci.co.uk/news/technology/rss.xml')
    root = etree.fromstring(response.content)
    try:
        for newsItem in root.iter('item'):
            data = {}
            data['title'] = newsItem.find('title').text
            data['description'] = newsItem.find('description').text
            data['url'] = newsItem.find('link').text
            data['publishedAt'] = newsItem.find('pubDate').text
            data['urlToImage'] = newsItem.find('media:thumbnail',newsItem.nsmap).attrib['url']
            mainData['articles'].append(data)
    except:
        print "Error in Tech",sys.exc_info()[0]

    response = requests.get('http://feeds.feedburner.com/gadgets360-latest')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('fullimage').text
        mainData['articles'].append(data)

    response = requests.get('https://www.hindustantimes.com/rss/tech/rssfeed.xml')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('media:content',newsItem.nsmap).attrib['url']
        mainData['articles'].append(data)

    response = requests.get('https://www.techradar.com/rss')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        data = {}
        data['title'] = newsItem.find('title').text
        data['description'] =  newsItem.find('description').text
        data['url'] = newsItem.find('link').text
        data['urlToImage'] = newsItem.find('enclosure').attrib['url']
        mainData['articles'].append(data)

    response = requests.get('http://feeds.feedburner.com/TechCrunch/')
    root = etree.fromstring(response.content)
    for newsItem in root.iter('item'):
        try:
            data = {}
            data['title'] = newsItem.find('title').text
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
    #json_data = json.dumps(newsObj)
    rec_id = collection.insert_one(newsObj)
    print("Data Inserted with record id",rec_id)
    #print json_data
    time.sleep(300)
