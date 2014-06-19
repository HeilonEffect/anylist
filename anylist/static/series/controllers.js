var series = angular.module('series', ['ngCookies']).run(function ($http, $cookies) {
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
});

series.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

series.controller('SeriesCtrl', function ($scope, $http, $location, $compile, $element) {
	$scope.tablehead = ['Number', 'Name', 'Datetime', 'Length'];
	
	// Получаем список серий
	$http.get($location.absUrl() + 'list').success(function (data) {
		$scope.num_seasons = data.length + 1;
		$scope.seasons = data;
		// если серий не ноль и у нас есть права на добавление и редактирование
		// добавляем соотвествующие заголовки в таблицу
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

	// Показываем/скрываем главное меню
	$scope.show_menu = function () {
		var elem = document.getElementsByTagName('details')[0];
		var el = document.getElementById('space');
		if (elem.style.visibility == 'hidden') {
			elem.style.visibility = "visible";
			el.style.visibility = 'visible';
		} else {
			elem.style.visibility = "hidden";
			el.style.visibility = 'hidden';
		}
	}

	// скрываем главное меню по нажатию на на свободную область
	$scope.hide_menu = function () {
		document.getElementsByTagName('details')[0].style.visibility = "hidden";
		document.getElementById("space").style.visibility = "hidden";
	}

	$scope.logout = function () {
		var url = window.location.pathname;
		if (url.endsWith("/"))
			window.location.pathname += "logout";
		else
			window.location.pathname += "/logout";
	}

	$scope.login = function () {
	}

	$scope.searcher = function () {
		;
	}

	$scope.add_serie_new_vol = function (data, elem) {
		// Посылаем серию из нового сезона
		data = "name=" + data['name'] + "&start_date=" + data['start_date'] +
			"&length=" + data['length'] + "&number=1";
		data += "&product=" + $location.absUrl().split("/")[4].split("-")[0];
 		data += "&num_season=" + elem.num_seasons;
	 	data = data.replace("undefined", "", "g");

		$http({
			method: "POST",
			url: $location.absUrl() + "add",
			data: data,
			headers: {
				'Content-Type': "application/x-www-form-urlencoded"
			}
		});
	}

	$scope.add_serie = function (data, elem) {
		// посылаем новую серию из существующего сезона
		var d = data;
		data = "name=" + data['name'] + "&start_date=" + data['start_date'] +
			 "&length=" + data['length'] + "&num_season=" + elem.season.number;
		data = data.replace("undefined", "", "g");

		var number = elem.season.series.length + 1;
		data += "&number=" + number;
		data += "&product=" + $location.absUrl().split("/")[4].split("-")[0];
		
		$http({
			method: "POST",
			url: $location.absUrl() + "add",
			data: data,
			headers: {
				'Content-Type': "application/x-www-form-urlencoded"
			}
		}).success(function (data, status, headers, config) {
			// в случае успешного добавления серии немедленно отображаем её на странице
			$scope.seasons[elem.season.number - 1].series.unshift(
				{'number': number, 'name': d['name'], 'start_date': d['start_date'],
				'length': d['length'], 'imgUrl': '/static/edit.png', 'listed': 'Add to List'});
		}).error(function (data, status, headers, config) {
			// в случае неуспешного недобавления подсвечиваем нужное поле
			for (var key in data) {
				var el = document.querySelectorAll('input[name="' + key + '"]')[1];
				el.style.border = "2px solid red";
				el.value = data[key];
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
