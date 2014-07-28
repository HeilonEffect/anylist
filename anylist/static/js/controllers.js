var defaultApp = angular.module('defaultApp', [
	'angularFileUpload', 'ngCookies'
]).run(function ($http, $cookies) {
	$http.defaults.headers.post['X-CSRFToken'] = '{{ csrf_token }}';
});

defaultApp.config(function ($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});


defaultApp.directive('ngThumb', ['$window', function($window) {
        var helper = {
            support: !!($window.FileReader && $window.CanvasRenderingContext2D),
            isFile: function(item) {
                return angular.isObject(item) && item instanceof $window.File;
            },
            isImage: function(file) {
                var type = '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
            }
        };

        return {
            restrict: 'A',
            template: '<canvas/>',
            link: function(scope, element, attributes) {
                if (!helper.support) return;

                var params = scope.$eval(attributes.ngThumb);

                if (!helper.isFile(params.file)) return;
                if (!helper.isImage(params.file)) return;

                var canvas = element.find('canvas');
                var reader = new FileReader();

                reader.onload = onLoadFile;
                reader.readAsDataURL(params.file);

                function onLoadFile(event) {
                    var img = new Image();
                    img.onload = onLoadImage;
                    img.src = event.target.result;
                }

                function onLoadImage() {
                    var width = params.width || this.width / this.height * params.height;
                    var height = params.height || this.height / this.width * params.width;
                    canvas.attr({ width: width, height: height });
                    canvas[0].getContext('2d').drawImage(this, 0, 0, width, height);
                }
            }
        };
}]);

defaultApp.controller('DefaultCtrl', ['$scope', '$http', '$location',
	function ($scope, $http, $location) {
		$scope.hidden_menu = false;
		$scope.visibility_form = false;
		$scope.visibility_user = false;
				
		$scope.show_menu = function () {
			$scope.hidden_menu = !$scope.hidden_menu;
		}

		$scope.show_user_menu = function () {
			$scope.visibility_user = true;
		}

		$scope.hide_user_menu = function () {
			$scope.visibility_user = false;
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

/*
	Список продуктов конкретной категории
*/
defaultApp.controller('ListCtrl', ['$scope', '$http', '$location', 'FileUploader',
	function ($scope, $http, $location, FileUploader) {
		$scope.panel_visibility = false;
		$scope.edit_visibility = false;
		$scope.add_form_visible = false;

		$scope.uploader = new FileUploader();
		$scope.uploader.queueLimit = 1;
		$scope.uploader.removeAfterUpload = true;

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

		$scope.mouse_over = function (elem) {
			elem.product.edit_btn = true;
		}

		$scope.mouse_leave = function (elem) {
			elem.product.edit_btn = false;
		}

		$scope.show_edit_form = function (elem) {
			$scope.visibility_form = true;
		}

		$http.get('/api/genres/category:' + category).success(function (data) {
			$scope.genre_groups = data;
			$scope.all_genres = [];
			for (var i in data)
				for (var j in data[i].genres) {
					$scope.all_genres.push(data[i].genres[j]);
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

		$scope.remove_image = function () {
			$scope.uploader.removeFromQueue(0);
		}

		$http.get('/api/products/category:' + url).success(function (data) {
			$scope.products = data;
			for (var i in data) {
				$scope.products[i].avatar = "/media/" + data[i].avatar.split('/').pop();
				$scope.products[i].edit_btn = false;
			}
		});

		$scope.show_panel = function () {
			$scope.panel_visibility = !$scope.panel_visibility;
		}
		
		$scope.add_form = function () {
			$scope.add_form_visible = !$scope.add_form_visible;
			// window.location.href = $location.absUrl().split('/').slice(0, 4).join('/') + "/add";
		}


		$http.get('/api/categories').success(function (data) {
			for (var i in data)
				for (var key in data[i]['categories'])
					if (data[i]['categories'][key].url == category)
						$scope.category_id = data[i]['categories'][key].id;
		});

		$scope.add_product = function () {
			$scope.product['category'] = $scope.category_id;
			$scope.uploader.queue[0].alias = "avatar";
			$scope.uploader.queue[0].formData.push($scope.product);
			$scope.uploader.queue[0].url = "/api/products";
			console.log($scope.uploader.queue[0].formData);
			$scope.uploader.uploadAll();
		}
	}
]);

/*
	Добавление/изменение продукта
*/
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

		var is_edit = !window.location.pathname.endsWith('/add/');
		var id = window.location.pathname.split('/')[2].split('-')[0]

		if (is_edit) {;
			$http.get('/api/products/id:' + id).success(function (data) {
				$scope.product = data;
				var tmp = data.avatar.split('/');
				$scope.product.avatar = '/media/' + tmp[tmp.length - 1];
				// $scope.active_genres = $scope.product.genres;

				$http.get('/api/genres').success(function (data) {
					$scope.active_genres = data.filter(function (elem) {
						return $scope.product.genres.indexOf(elem.id) != -1;
					});
					var ids = $scope.active_genres.map(function (elem) {
						return elem.id;
					});

					$http.get('/api/genres/category:' + category).success(function (data) {
						$scope.genre_groups = data;
						$scope.genre_groups = data.map(function (group) {
							group.genres = group.genres.map(function (genre) {
								if (ids.indexOf(genre.id) != -1)
									genre.checked = true;
								return genre;
							});
							return group;
						});
					});
				});
			});
		} else {
			$http.get('/api/genres/category:' + category).success(function (data) {
				$scope.genre_groups = data;
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

		$scope.add_product = function () {
			if (!$scope.product)
				$scope.product = {};
			$scope.product['genres'] = $scope.active_genres.map(function (elem) {
				return elem.id;
			});
			if (is_edit) {
				console.log($scope.product);
				console.log($scope.uploader);
				if ($scope.uploader.queue.length > 0) {
					$scope.uploader.queue[0].alias = 'avatar';
					$scope.uploader.queue[0].formData.push($scope.product);
					$scope.uploader.queue[0].url = "/api/products/id:" + id;
					$scope.uploader.queue[0].method = "PUT";
				}
				$http({
					method: "PUT",
					url: "/api/products/id:" + id,
					data: $scope.product
				});
			} else {
				$scope.product['category'] = $scope.category_id;
				$scope.uploader.queue[0].alias = "avatar";
				$scope.uploader.queue[0].formData.push($scope.product);
				$scope.uploader.queue[0].url = "/api/products";
				console.log($scope.uploader.queue[0]);
				$scope.uploader.uploadAll();
			}
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