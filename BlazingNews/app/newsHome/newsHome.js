'use strict';

var app = angular.module('myApp.newsHome', ['ngRoute'])

app.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/newsHome', {
    templateUrl: 'newsHome/newsHome.html',
    controller: 'newsHomeCtrl'
  });
}])

app.controller('newsHomeCtrl',['$scope','newsFactory',function($scope,newsFactory) {
  newsFactory.getNewsFactory('all',function(r){
    $scope.newsSource = r;
  });
  /*var allNews = null;
  var sportsNews = null;
  var sciNews = null;
  var techNews = null;
  var bussNews = null;
  var healthNews = null;
  var genNews = null;
  var entNews = null;
  var newsSource = null;
  $http.get("http://192.168.0.108:3000/all").then(function(response){
    allNews = response.data.articles;
    allNews.category = "all";
  });

  $http.get("http://192.168.0.108:3000/sport").then(function(response){
    sportsNews = response.data.articles;
    sportsNews.category = "sports";
  });
  
  $http.get("http://192.168.0.108:3000/science").then(function(response){
    sciNews = response.data.articles;
    sciNews.category = "science";
  });

  $http.get("http://192.168.0.108:3000/technology").then(function(response){
    techNews = response.data.articles;
    techNews.category = "tech";
  });

  $http.get("http://192.168.0.108:3000/business").then(function(response){
    bussNews = response.data.articles;
    bussNews.category = "buss";
  });

  $http.get("http://192.168.0.108:3000/health").then(function(response){
    healthNews = response.data.articles;
    healthNews.category = "health";
  });
  
  $http.get("http://192.168.0.108:3000/entertainment").then(function(response){
    entNews = response.data.articles;
    entNews.category = "ENTERTAINMENT";
  });

  $http.get("http://192.168.0.108:3000/general").then(function(response){
    genNews = response.data.articles;
    genNews.category = "GENERAL_NEWS";
  });
  var newsSource = [allNews,sportsNews,sciNews,techNews,bussNews,healthNews,entNews,genNews];
  
  this.getData = function(source){
    switch(source){
      case "allNews":
      newsSource = allNews;
      break;
      case "sportsNews":
      newsSource = sportsNews;
      break;
      case "sciNews":
      newsSource = sciNews;
      break;
      case "techNews":
      newsSource = techNews;
      break;
      case "bussNews":
      newsSource = bussNews;
      break;
      case "healthNews":
      newsSource = healthNews;
      break;
      case "entNews":
      newsSource = entNews;
      break;
      case "genNews":
      newsSource = genNews;
      break;
    }
  };
  
  this.isSelected = function(data){
    return true;
  }
  this.filText = '';
  this.select = function(setTab){
    if(setTab === 2){
      this.filText = "GENERAL_NEWS";
    }
  }
*/
$scope.getNews = function(source){
  newsFactory.getNewsFactory(source,function(r){
    $scope.newsSource = r;
  });
  
};
}]);

app.factory('newsFactory',['$http','$log', function($http, $log){
  $log.log("Instantiating newsFactory");
  var articles;
  var newsService = {};
  newsService.getNewsFactory = function(source,cb){
    $http({
      url: "http://ec2-54-244-2-94.us-west-2.compute.amazonaws.com:3000/"+source,
      method: 'GET'
    }).then(function(resp){
      cb(resp.data);
    },function(resp){
      $log.error("Error");
    });
  };
  return newsService;
}]);
