var series = angular.module('series', ['ngCookies']).run(function ($http, $cookies) {
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
});

series.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

series.controller('SeriesCtrl', function ($scope, $http, $location) {
	$scope.tablehead = ['Number', 'Name', 'Datetime', 'Length'];
	
	$http.get($location.absUrl() + 'list').success(function (data) {
		$scope.seasons = data;
		// если серий не ноль и у нас есть права на добавление и редактирование
		if (data.length > 0)
			if ('listed' in data[0].series[0]) {
				$scope.tablehead = ['Number', 'Name', 'Datetime', 'Length', 'Edit', 'Add'];
			}
	});

	// отрисовываем боковое меню
	var head_url = $location.absUrl().split("/").slice(0, 5).join("/");
	$scope.categories = [
		{'title': 'Main', 'url': head_url},
		{'title': 'Series', 'url': ''},
		{'title': 'Heroes', 'url': [head_url, 'heroes'].join('/')},
		{'title': 'Creators', 'url': [head_url, 'creators'].join('/')}
	];

	$scope.add_serie = function (data, elem) {
		data = "number=" + data['number'] + "&start_date=" + data['start_date'] +
			 "&length=" + data['length'] + "&season=" + elem.season.number;
		$http({
			method: "POST",
			url: $location.absUrl() + "add",
			data: data,
			headers: {
				'Content-Type': "application/x-www-form-urlencoded"
			}
		});
	}

	$scope.edit = function (elem) {
		var season = elem.$parent.season.number;
		var serie = elem.serie.number;

		var len_ser = elem.$parent.season.series.length;
		var len_seasons = elem.$parent.$parent.seasons.length;

		if ($scope.seasons[len_seasons - season].series[len_ser - serie].imgUrl.endsWith("edit.png")) {
			$scope.seasons[len_seasons - season].series[len_ser - serie].imgUrl = "/static/check.png";
		} else {
			$scope.seasons[len_seasons - season].series[len_ser - serie].imgUrl = "/static/edit.png";
		}
	}

	$scope.add_to = function (elem) {
		var season = elem.$parent.season;
		var serie = elem.serie;
		var product = $location.absUrl().split("/")[4].split("-")[0];

		var len_ser = elem.$parent.season.series.length;
		var len_seasons = elem.$parent.$parent.seasons.length;

		var txt = elem.$$watchers[0].last;
		var url;
		if (txt == "Удалить из списка")
			url = "/mylist/series/del";
		else
			url = "/mylist/series/add";

		$http({
			method: "POST",
			url: url,
			data: "number="+ serie.number+ "&season="+ season.number+ "&product="+ product,
			headers: {
				//'Content-Type': 'multipart/form-data'
				'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
			}
		}).success(function (data) {
			if (url.endsWith("add"))
				$scope.seasons[len_seasons - season.number].series[len_ser - serie.number].listed = "Удалить из списка";
			else
				$scope.seasons[len_seasons - season.number].series[len_ser - serie.number].listed = "Добавить в список";
		});
	}
});
