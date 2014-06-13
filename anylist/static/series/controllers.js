var series = angular.module('series', []);

series.controller('SeriesCtrl', function ($scope, $http, $location) {
	var product = $location.absUrl().split("/")[4].split("-")[0];
	$http.get('/api/product:' + product + '/seasons').success(function (data) {
		$scope.seasons = data;
	});
});