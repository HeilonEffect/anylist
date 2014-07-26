var defaultApp = angular.module('defaultApp', [
	'angularFileUpload', 'ngCookies'
]).run(function ($http, $cookies) {
	$http.defaults.headers.post['X-CSRFToken'] = '{{ csrf_token }}';
});

defaultApp.config(function ($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

defaultApp.controller('DefaultCtrl', ['$scope', '$http', '$location',
	function ($scope, $http, $location) {
		$scope.hidden_menu = false;
		$scope.visibility_form = false;
		$scope.visibility_user = false;
				
		$scope.show_menu = function () {
			$scope.hidden_menu = !$scope.hidden_menu;
		}

		$scope.show_user_menu = function () {
			$scope.visibility_user = !$scope.visibility_user;
		}

		$http.get('/api/categories/?format=json').success(function (data) {
			$scope.category_group = data;
		});

		$scope.auth_me = function () {
			var url = $location.absUrl()
			if ($scope.auth['is_reg'])
				url += 'register/';
			else
				url += 'login/';
			var data = '';
			for (var key in $scope.auth)
				data += ("&" + key + '=' + $scope.auth[key]);
			data = data.replace('undefined', '').slice(1);
			$http({
				method: "POST",
				url: url,
				data: data,
				headers: {
					"Content-Type": "application/x-www-form-urlencoded"
				}
			}).success(function (data) {
				window.location.href = window.location.href;
			});
		}

		$scope.logout = function () {
			window.location.pathname += "logout";
		}

		$scope.login = function () {
			$scope.visibility_form = !$scope.visibility_form;
		}
		$scope.searcher = function () {
			$http.get('/search?key=' + $scope.search_data).success(function (data) {
				$scope.search_result = data;
			});
		}
	}
]);

defaultApp.controller('ListCtrl', ['$scope', '$http', '$location',
	function ($scope, $http, $location) {
		$scope.panel_visibility = false;
		$scope.active_genres = {};
		$scope.active_limits = {};
		var limits = $location.absUrl().split('/').slice(5);
		var lims = [];
		var genres = [];
				
		if (limits.indexOf('old_limit') != -1)
			lims = limits[limits.indexOf('old_limit') + 1].split(',');
		if (limits.indexOf('genres') != -1)
			genres = limits[limits.indexOf('genres') + 1].split(',');
		
		for (var i in lims)
			$scope.active_limits[lims[i]] = true;
		for (var i in genres)
			$scope.active_genres[genres[i]] = true;

		var category = $location.absUrl().split('/');
		category = category[3];

		$http.get('/api/genres/category:' + category).success(function (data) {
			$scope.genre_groups = data;
			for (var i in data)
				for (var j in data[i].genres) {
					if (genres.indexOf(data[i].genres[j].name) != -1)
						$scope.genre_groups[i].genres[j].checked = true;
					else
						$scope.genre_groups[i].genres[j].checked = false;
				}
		});

		$http.get('/api/raitings').success(function (data) {
			$scope.raiting = data;
			for (var i in data) {
				if (lims.indexOf(data[i].name) != -1)
					$scope.raiting[i].checked = true;
				else
					$scope.raiting[i].checked = false;
			}
		});

		$scope.start_filter = function (elem) {
			// По нажатию на флажок - фиксируем активный элемент
			if (elem.genre)
				$scope.active_genres[elem.genre.name] = !$scope.active_genres[elem.genre.name];

			if (elem.old_limit)
				$scope.active_limits[elem.old_limit.name] = !$scope.active_limits[elem.old_limit.name];
			var next_url = '/filter';

			// Удаляем элемнты, равные false
			var tmp = Object.keys($scope.active_limits).filter(function (elem) {
				return $scope.active_limits[elem];
			});
			// Если елемнты ещё остались - заносим их в схему url'a
			if (tmp.length > 0) {
				next_url += '/old_limit/';
				for (var i in tmp)
					next_url += tmp[i] + ',';
				next_url = next_url.slice(0, next_url.length - 1);
			}
			tmp = Object.keys($scope.active_genres).filter(function (elem) {
				return $scope.active_genres[elem];
			});
			if (tmp.length > 0) {
				next_url += '/genres/';
				for (var i in tmp)
					next_url += tmp[i] + ',';
				next_url = next_url.slice(0, next_url.length - 1);
			}
			if (next_url == '/filter')
				next_url = '';
			window.location.href = $location.absUrl().split('/').slice(0, 4).join('/') + next_url + '/';
		}

		var url = $location.absUrl().split('/').slice(3).join('/');

		$http.get('/api/products/category:' + url).success(function (data) {
			$scope.products = data;
			for (var i in data)
				$scope.products[i].avatar = "/media/" + data[i].avatar.split('/').pop();
		});

		$scope.show_panel = function () {
			$scope.panel_visibility = !$scope.panel_visibility;
		}
		
		$scope.add_form = function () {
			window.location.href = $location.absUrl().split('/').slice(0, 4).join('/') + "/add";
		}
	}
]);

defaultApp.controller('AddFormCtrl', function ($scope, $http, $location, FileUploader) {
		$scope.uploader = new FileUploader();

		$scope.visibility_genres = false;
		$scope.active_genres = [];

		var category = window.location.pathname.split('/')[1];

		// Убрать впоследствии
		$http.get('/api/categories').success(function (data) {
			for (var i in data)
				for (var key in data[i]['categories'])
					if (data[i]['categories'][key].url == category)
						$scope.category_id = data[i]['categories'][key].id;
		});

		$scope.show_genres = function () {
			$scope.visibility_genres = !$scope.visibility_genres;
		}

		if (window.location.pathname.split('/').length > 3) {
			var id = window.location.pathname.split('/')[2].split('-')[0]
			$http.get('/api/products/id:' + id).success(function (data) {
				$scope.product = data;
				var tmp = data.avatar.split('/');
				$scope.product.avatar = '/media/' + tmp[tmp.length - 1];
				$scope.active_genres = $scope.product.genres;
			});
		}

		$scope.select_genre = function (genre) {
			if (genre.checked)
				$scope.active_genres.push(genre);
			else
				$scope.active_genres = $scope.active_genres.filter(function (elem) {
					return elem.name != genre.name;
				});
		}

		$scope.select_raiting = function (limit) {
			if (!$scope.product)
				$scope.product = {};
			$scope.product['old_limit'] = limit;
		}

		$http.get('/api/raitings/').success(function (data) {
			$scope.raiting = data;
		});

		$http.get('/api/genres/category:' + category).success(function (data) {
			$scope.genre_groups = data;
		});

		$scope.add_product = function () {
			if (!$scope.product)
				$scope.product = {};
			$scope.product['genres'] = $scope.active_genres.map(function (elem) {
				return elem.id;
			});
			$scope.product['category'] = $scope.category_id;
			$scope.uploader.queue[0].alias = "avatar";
			$scope.uploader.queue[0].formData.push($scope.product);
			$scope.uploader.queue[0].url = "/api/products";
			console.log($scope.product);
			$scope.uploader.uploadAll();
		}
	}
);


/*
	Отображает описание продукта
*/
defaultApp.controller('DetailCtrl', ['$scope', '$http', '$location',
	function ($scope, $http, $location) {
		$scope.statuses = ['Planned', 'Watch', 'ReWatching', 'Watched', 'Deffered', 'Dropped'];

		var id = window.location.pathname.split('/')[2].split('-')[0];

		$http.get('/api/products/id:' + id + '/status').success(function (data) {
			$scope.active_status = data['status'];
		});

		$http.get('/api/products/id:' + id).success(function (data) {
			$scope.product = data;
		});

		$scope.contents = [
			{'name': 'Description', 'url': ''},
			{'name': 'Series', 'url': 'series'},
			{'name': 'Heroes', 'url': 'heroes'},
			{'name': 'Creators', 'url': 'creators'}
		];

		$http.get('/api/genres').success(function (data) {
			$scope.genres = data;
		});

		$scope.category = window.location.pathname.split('/')[1];
		$scope.raiting = ['G', 'PG', 'PG-13', 'R', 'NC-17'];

		$scope.status_move = function (elem) {
			$http({
				method: "POST",
				url: $location.absUrl() + "status",
				data: 'name=' + elem.status,
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}).success(function (data) {
				$scope.active_status = elem.status;
			});
		}
	}
]);