var defaultApp = angular.module('defaultApp', [
	'ngCookies',
    'angularFileUpload',
    'ngQuickDate'
]);

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


defaultApp.config(function ($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

defaultApp.controller('DefaultCtrl', ['$scope', '$http', '$location', '$window',
	function ($scope, $http, $location, $window) {
		$scope.hidden_menu = false;
		$scope.visibility_form = false;
		$scope.visibility_user = false;
        $scope.username = $window.localStorage.username;
				
		$scope.show_menu = function () {
			$scope.hidden_menu = !$scope.hidden_menu;
		}

		$scope.show_user_menu = function () {
			$scope.visibility_user = true;
		}

		$scope.hide_user_menu = function () {
			$scope.visibility_user = false;
		}

		$http.get('/api/categories').success(function (data) {
			$scope.category_group = data;
		});

		$scope.auth_me = function () {
            var url = $location.absUrl();
            var data = "username=" + $scope.auth['username'] + "&password=" + $scope.auth['password'];
            $http.post('/api-token-auth/', {
                username: $scope.auth['username'],
                password: $scope.auth['password']
            }, {
                headers:{
                    'Content-Type': 'application/json'
                }
            }).success(function (data) {
                console.log(data);
                $window.localStorage['token'] = data['token'];
                $window.localStorage['username'] = $scope.auth['username'];
                $http.defaults.headers.common.Authorization = 'Token ' + data['token'];
            });
		}


		$scope.logout = function () {
			window.location.pathname += "logout";
		}

		$scope.login = function () {
			$scope.visibility_form = !$scope.visibility_form;
		}
		$scope.searcher = function () {
            if ($scope.search_data.length > 1)
                $http.get('/api/search?product=' + $scope.search_data).success(function (data) {
                    $scope.search_result = data;
                });
            else
                $scope.search_result = [];
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

        $scope.token = localStorage.token;
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

		$scope.show_edit_form = function (elem, $event) {
			$scope.add_form_visible = true;
			$scope.product = elem.product;
			$event.preventDefault();
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

		$http.get('/api/products/category:' + url, {headers: {'Authorization': 'Token ' + localStorage.token}}
        ).success(function (data) {
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
		}


		$http.get('/api/categories').success(function (data) {
			for (var i in data)
				for (var key in data[i]['categories'])
					if (data[i]['categories'][key].url == category)
						$scope.category_id = data[i]['categories'][key].id;
		});

		$scope.add_to_list = function (elem, $event, user_list) {
            // Добавление продукта со страницы списка
			$http({
				method: "POST",
				url: "/api/userlist/product:" + elem.product.id,
				data: "name=Planned",
				headers: {
					"Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": 'Token ' + localStorage.token
				}
			}).success(function (data) {
                data['status'] = 'Planned';
                user_list[data['product']] = data;
            });
			$event.preventDefault();
		}

		$http.get('/api/userlist?category=' + category, {
            headers: {'Authorization': 'Token ' + localStorage.token}
        }).success(function (data) {
			var statuses = ["", "Planned", "Watch", "ReWatching", "Watched", "Deffered", "Dropped"];
			$scope.user_list = {};
			for (var i in data) {
				var key = '' + data[i].product;
				data[i].status = statuses[data[i].status];
				$scope.user_list[key] = data[i];
			}
		});


		$scope.add_product = function () {
			$scope.product['category'] = $scope.category_id;
			$scope.uploader.queue[0].alias = "avatar";
			$scope.uploader.queue[0].formData.push({'data': JSON.stringify($scope.product)});
			$scope.uploader.queue[0].url = "/api/products";
			$scope.uploader.uploadAll();
		}
	}
]);

/*
	Отображает описание продукта
*/
defaultApp.controller('DetailCtrl', ['$scope', '$http', '$location', '$window',
	function ($scope, $http, $location, $window) {
		$scope.statuses = ['Add To List', 'Planned', 'Watch', 'ReWatching', 'Watched', 'Deffered', 'Dropped'];
        $scope.token = $window.localStorage['token'];

		var id = window.location.pathname.split('/')[2].split('-')[0];

		$http.get('/api/products/id:' + id + '/status', {headers: {
            'Authorization': 'Token ' + $scope.token
        }}).success(function (data) {
			$scope.active_status = data['status'];
		});

		$http.get('/api/products/id:' + id, {
            headers: {'Authorization': 'Token ' + $scope.token}
        }).success(function (data) {
			$scope.product = data;
		});

        $http.get('/api/userlist?product=' + id, {
            headers: {'Authorization': 'Token ' + $scope.token}
        }).success(function(data) {
            if (data[0])
                $scope.active_status = $scope.statuses[data[0].status];
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

        // Смена статуса продукта
        $scope.status_move = function (elem, active_status) {
            var metod = 'POST'
            if (active_status)
                metod = "PUT";
            if (elem.status != $scope.statuses[0])
                $http({
                    method: metod,
                    url: "/api/userlist/product:" + id,
                    data: "name=" + elem.status,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': 'Token ' + $scope.token
                    }
                });
        }

        $http.get('/api/seasons?product=' + id, { headers: {
            'Authorization': 'Token ' + $scope.token
        }}).success(function (data) {
			$scope.seasons = data;
			var count = 0;
			for (var i in data)
				for (var j in data[i].series) {
					count++;
					if (!data[i].series[j]['length'])
						$scope.seasons[i].series[j]['length']= " ";
					if (data[i].series[j].start_date) {
						var tmp = data[i].series[j].start_date.slice(0, 10)
						$scope.seasons[i].series[j].start_date = tmp;
					}
				}
			$scope.count_series = count;
		});

        // Создание нового сезона
        $scope.create_season = function () {
			$http({
				method: "POST",
				url: "/api/seasons",
				data: "product=" + id,
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Token ' + $scope.token
				}
			}).success(function (data) {
				$scope.seasons.unshift(data);
			});
		}

        $scope.serie_mouse_enter = function (serie) {
			serie.edit = true;
		}

		$scope.serie_mouse_leave = function (serie) {
			serie.edit = false;
		}

		$scope.show_menu = function (serie) {
			serie.menu = !serie.menu;
		}

        // Добавление новой серии
		$scope.create_serie = function (season) {
			// Добавляем отсутсвующий ноль
			var start_date = season.new_serie.start_date.toLocaleString().split(' ').join(' 0') || "";

			var data = "number=" + season.new_serie.number + "&name=" + season.new_serie.name +
				"&start_date=" + start_date + "&length=" + season.new_serie.length;
			data = data.replace("undefined", "", "g");
			data += "&season=" + season.id;
			$http({
				method: "POST",
				url: "/api/series",
				data: data,
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Token ' + $scope.token
				}
			}).success(function (data) {
                data.start_date = data.start_date.slice(0, 10);
                season.series.unshift(data);
			});
		}

        $scope.edit_serie = function (serie) {}

        $scope.add_to_list_serie = function (serie) {
            $http({
                method: "POST",
                url: "/api/serielist",
                data: "serie=" + serie.id + "&product=" + id,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Token ' + $scope.token
                }
            }).success(function (data) {
                $scope.readed_series++;
                $scope.serielist['' + data.serie] = data;
            });
        }

        $scope.del_from_list_serie = function (serie, serielist) {
            console.log(serie);
            $http({
                method: "DELETE",
                url: "/api/serielist/serie:" + serie.id,
                data: "",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Token ' + $scope.token
                }
            }).success(function (data) {
                delete serielist[serie.id];
                $scope.readed_series--;
            });
        }

        $scope.show_editing = function (serie) {
            serie.new_version = {number: serie.number, name: serie.name, start_date: serie.start_date, length: serie.length};
            serie.editing = !serie.editing;
        }

        $http.get('/api/serielist?user=' + localStorage.username, {headers: {
            'Authorization': 'Token ' + $scope.token
        }}).success(function (data) {
            $scope.readed_series = data.length;
            $scope.readed_series_old = data.length;
            var tmp = {};
            for (var i in data)
                tmp['' + data[i]['serie']] = data;
            $scope.serielist = tmp;
        });

        $scope.submit_serie = function (serie) {
            var start_date = serie.new_version.start_date.toLocaleString().split(' ').join(' 0') || "";
            var data = "number=" + serie.new_version.number + "&name=" + serie.new_version.name + "&start_date=" +
                start_date + "&length=" + serie.new_version.length + "&season=" + serie.season_id;
            $http({
                method: "PUT",
                url: "/api/series/id:" + serie.id,
                data: data,
                headers: {
                    'Authorization': 'Token ' + localStorage.token,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).success(function (data) {
                serie.editing = false;
                serie.number = serie.new_version.number;
                serie.name = serie.new_version.name;
                serie.start_date = serie.new_version.start_date;
                serie['length'] = serie.new_version['length'];
                serie.new_version = None;
            });
        }

        // Указывает произвольное число серий
        $scope.add_series = function () {
            console.log($scope.readed_series);
            if ($scope.readed_series > $scope.readed_series_old) {
                console.log('Просмотренных серий увеличилось');
                var series = [];
            } else {
                console.log('Просмотренных серий уменьшилось');
            }
        }

        // Добавление следующей серии в список просмотренных
        $scope.plus_one = function () {
            var series = [];
            var maximum = 0;
            var next_serie = {};
            for (var i in $scope.seasons)
                for (var j = $scope.seasons[i].series.length - 1; j >= 0; j--)
                    if (!$scope.serielist[$scope.seasons[i].series[j].id])
                        series.push($scope.seasons[i].series[j]);
                    else {
                        maximum = $scope.seasons[i].series[j].number;
                        if (j > 0)
                            next_serie = $scope.seasons[i].series[j - 1];
                    }
            if (series[series.length - 1].number > maximum) {
                $http({
                    method: "POST",
                    url: "/api/serielist",
                    data: "serie=" + next_serie.id + "&product=" + id,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': 'Token ' + $scope.token
                    }
                }).success(function (data) {
                    $scope.readed_series++;
                    $scope.serielist['' + data.serie] = data;
                });
            } else {
                var max_serie = series.reduce(function (previousValue, currentValue, index, array) {
                    return previousValue.id > currentValue.id ? previousValue : currentValue;
                });
                $http({
                    method: "POST",
                    url: "/api/serielist",
                    data: "serie=" + max_serie.id + "&product=" + id,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': 'Token ' + $scope.token
                    }
                }).success(function (data) {
                    $scope.readed_series++;
                    $scope.serielist['' + data.serie] = data;
                });
            }
        }
	}
]);


defaultApp.controller('ProfileController', ['$scope',
    function ($scope) {
        ;
    }]);

defaultApp.controller('UserCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.statuses = ['', 'Planned', 'Watch', 'ReWatching', 'Watched', 'Deffered', 'Dropped'];
        $scope.statuses_lower = ['', 'planned', 'watch', 'rewatching', 'watched', 'deffered', 'dropped'];
        var arr = window.location.pathname.split('/');
        var category = arr[3];
        var status = $scope.statuses_lower.indexOf(arr[4]);

        $http.get('/api/userlist?status=' + status + '&category=' + category, {headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + localStorage.token
        }}).success(function (data) {
            $scope.user_list = data;
        });
    }]);