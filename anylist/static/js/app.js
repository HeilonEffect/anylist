var anylistApp = angular.module('anylistApp', [
    'ngRoute',
    'defaultApp',
    'angularFileUpload',
    'ngQuickDate'
]);

anylistApp.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $locationProvider.html5Mode(true);
        $routeProvider.
            when('/', {
                templateUrl: 'index.html',
                controller: 'DefaultCtrl'
            }).
            when('/user/profile', {
                templateUrl: 'profile.html',
                controller: 'ProfileController'
            }).
            when('/profile/list/:category/:status', {
                templateUrl: 'user_list.html',
                controller: 'UserCtrl'
            }).
            when('/:paragraph', {
                templateUrl: 'list.html',
                controller: 'ListCtrl'
            }).
            when('/:paragraph/filter/:filter*', {
                templateUrl: 'list.html',
                controller: 'ListCtrl'
            }).
            when('/:paragraph/:product', {
                templateUrl: 'detail.html',
                controller: 'DetailCtrl'
            }).
            when('/:paragraph/:product/series', {
                templateUrl: 'series.html',
                controller: 'SeriesController'
            }).
            when('/:paragraph/:product/heroes', {
                templateUrl: 'heroes_list.html',
                controller: 'HeroController'
            }).
            when('/:paragraph/:product/creators', {
                templateUrl: 'creators_list.html',
                controller: 'CreatorController'
            }).
            when('/hero/:hero', {
                templateUrl: 'hero.html',
                controller: 'SingleHeroController'
            }).
            when('/creator/:creator', {
                templateUrl: 'creator.html',
                controller: 'SingleCreatorController'
            }).
            when('/404', {
                templateUrl: 'error.html'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]);