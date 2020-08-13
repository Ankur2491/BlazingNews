from pymongo import MongoClient
import json
import random
import time
import requests
client = MongoClient('mongodb://localhost:27017')
db=client.admin
newCol=db["News"]
x=newCol.find(sort=[('_id', -1)])
endpoint = "https://onesignal.com/api/v1/notifications"
appId = "5268fb98-e3f0-4590-b385-a7080d542381"
restKey = "ZWYwZjM2Y2EtYmRhMy00OGNmLTk5ZjgtZjJiMjdmNjhjNmZm"
headers = {'Content-type': 'application/json', 'Authorization': 'Basic ZWYwZjM2Y2EtYmRhMy00OGNmLTk5ZjgtZjJiMjdmNjhjNmZm'}
rand1=0
rand2=0
postData=None
res=None
while True:
    try:
        counter=0
        latestObj=None
        for doc in x:
            if counter==1:
                break
            latestObj = doc
            counter+=1
        y = latestObj["news"]
        intn = y[0]
        intn_articles = intn["articles"]
        ind = y[1]
        ind_articles = ind["articles"]
        bus = y[2]
        bus_articles = bus["articles"]
        ent = y[3]
        ent_articles = ent["articles"]
        health = y[4]
        health_articles = health["articles"]
        sci = y[5]
        sci_articles = sci["articles"]
        spo = y[6]
        spo_articles = spo["articles"]
        tech = y[7]
        tech_articles = tech["articles"]
        master_articles = [intn_articles,ind_articles,tech_articles]
        rand1 = random.randint(0,2)
        rand2 = random.randint(0,5)
        content=""
        if master_articles[rand1][rand2] is None:
            continue
        data = master_articles[rand1][rand2]
        if data['description'] == '':
            content = "Tap to open the app"
        else:
            content = data['description']
        postData = {'app_id':'5268fb98-e3f0-4590-b385-a7080d542381','headings':{'en': data["title"]}, 'contents': {'en': content}, 'data': {'targetUrl':data["url"]},'included_segments': ["Subscribed Users"],'big_picture':data["urlToImage"]}
        r = requests.post(endpoint, data=json.dumps(postData),headers=headers)
        res = r.content
        break
    except:
        print "ERROR: rand1:",rand1,"rand2:",rand2,"postData:",postData,"Response:",res
        break
