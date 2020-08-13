var express = require('express');
var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var MongoClient = require('mongodb').MongoClient;
var URL = 'mongodb://localhost:27017';
var allNews = null;
var redis = require('redis')
//create a Schema
var client = redis.createClient();
var newsSchema = new Schema({
  news: Array
});
var fs = require('fs')
var app = express();
//mongoose.connect(URL);
//var newsModel = mongoose.model('News',newsSchema);
/*newsModel.find({}, function(err,news){
  if(err) throw err;
  console.log(newsModel.db);
});*/
  var dbCall = function(){
  MongoClient.connect('mongodb://localhost:27017',function(err,client){
  if(err) throw err;
  var db = client.db('admin');
  db.collection('News').find({}).limit(1).sort({$natural:-1}).toArray(function(err,docs){
    allNews = JSON.stringify(docs[0]);
    console.log(allNews);
    client.close();
  })
  //var cursor = db.collection('News').find();
  //cursor.each(function(err,doc){
  //console.log(doc);
  //});
});
}
dbCall();
client.get('object',function(error,result){
    if (error) {
        console.log(error);
        throw error;
    }
console.log(result);
});
app.use(function(req,res,next){
  res.setHeader('Access-Control-Allow-Origin','*');
  next();
});
app.get('/business', function(req,res){
var ip = req.connection.remoteAddress; 
console.log(ip)
//console.log(allNews.news[2].articles);
res.send(JSON.parse(allNews).news[2].articles);
});

app.get('/entertainment', function(req,res){
  res.send(JSON.parse(allNews).news[3].articles);
  });

 app.get('/general', function(req,res){
  res.send(JSON.parse(allNews).news[1].articles);
  });

app.get('/health', function(req,res){
  res.send(JSON.parse(allNews).news[4].articles);
  });

app.get('/science', function(req,res){
  res.send(JSON.parse(allNews).news[5].articles);
  });

app.get('/sport', function(req,res){
  res.send(JSON.parse(allNews).news[6].articles);
  });

app.get('/technology', function(req,res){
  res.send(JSON.parse(allNews).news[7].articles);
  });
app.get('/all', function(req,res){
  res.send(JSON.parse(allNews).news[0].articles);
  });
app.get('/current', function(req,res){
  res.send(JSON.parse(allNews).news[8].articles);
  });
app.get('/offbeat', function(req,res){
  res.send(JSON.parse(allNews).news[9].articles);
  });


app.listen(3000, () => setInterval(function(){dbCall();},120000));
