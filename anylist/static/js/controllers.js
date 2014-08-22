var defaultApp = angular.module('defaultApp', []);

defaultApp.config(function ($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});


defaultApp.controller('DefaultCtrl', ['$scope', 'authProvider', 'workCategories', 'appSearch',
	function ($scope, authProvider, workCategories, appSearch) {
		$scope.hidden_menu = false;
		$scope.visibility_form = false;
		$scope.visibility_user = false;
        $scope.username = authProvider.getUsername();
        $scope.token = authProvider.getTokenValue();

		$scope.show_menu = function () {
			$scope.hidden_menu = !$scope.hidden_menu;
		};

		$scope.show_user_menu = function () {
			$scope.visibility_user = true;
		};

        $scope.categories = workCategories.getCategories();

        $scope.logout = function () {
            authProvider.logout();
        };

		$scope.auth_me = function () {
            authProvider.login($scope.auth);
		};

		$scope.login = function () {
			$scope.visibility_form = !$scope.visibility_form;
		};

        $scope.searcher = function () {
            appSearch.get_products_by_title($scope.search_data).then(function (data) {
                $scope.search_result = data;
            });
        };
	}
]);

/*
	Список продуктов конкретной категории
*/
defaultApp.controller('ListCtrl', ['$scope', '$http', 'urlFilters', 'workCategories', 'authProvider', 'oldLimits', 'userList', 'workGenres',
	function ($scope, $http, urlFilters, workCategories, authProvider, oldLimits, userList, workGenres) {
        var filters = urlFilters.getFilters();

        $scope.panel_visibility = false;
		$scope.add_form_visible = false;

        $scope.select_genre = function (genre) {
            $scope.product_genres['' + genre.id] = genre.name;
        };
        var category_name = workCategories.getCategoryNameByUrl();
        var category = workCategories.getCategoryId(category_name);

        $scope.mouse_over = function (elem) {
			elem.product.edit_btn = true;
		};

		$scope.mouse_leave = function (elem) {
			elem.product.edit_btn = false;
		};

        workGenres.get_genres_by_category(category).then(function (data) {
            $scope.genre_groups = data.map(function (group) {
                return {'genres': group.genres.map(function (genre) {
                    if (filters.genres.indexOf(genre.name) != -1)
                        genre.checked = true;
                    return genre;
                })};
            });
        });

        $scope.show_editing = function (product, event) {
            $scope.add_form_visible = !$scope.add_form_visible;
            $scope.editing_product = true;
            workGenres.get_genre_objects_by_ids(product.genres, category).then(function (data) {
                product.genres = data;
            });
            $scope.product = product;
            event.preventDefault();
        };

        oldLimits.getRaiting().success(function (data) {
            $scope.raiting = data.results;
        });

        // По нажатию на флажок с фильтрами совершаем переход
        $scope.start_filter = function (old_limit, genre) {
            if (genre)
                if (genre.checked)
                    filters.genres.push(genre.name);
                else
                    filters['genres'] = filters.genres.filter(function (data) {
                        return data != genre.name;
                    });
            if (old_limit)
                if (old_limit.checked)
                    filters.old_limit.push(old_limit.name);
                else
                    filters['old_limit'] = filters.old_limit.filter(function (data) {
                        return data != old_limit.name;
                    });
            urlFilters.forward_by_filters(filters, workCategories.getCategoryUrlByName(category_name));
        };

		$http.get('/api/products?category=' + category + "&genres=" + filters.genres.join(',') + "&old_limit=" + filters.old_limit.join(',')).success(function (data) {
			$scope.products = data.results;
		});

		$scope.show_panel = function () {
			$scope.panel_visibility = !$scope.panel_visibility;
		};
		
		$scope.add_form = function () {
			$scope.add_form_visible = !$scope.add_form_visible;
		};

        $scope.add_to_list = function (elem, $event, user_list) {
            userList.add_to_list(elem).then(function (data) {
                data['status'] = 'Planned';
                user_list[data['product'].id] = data;
            });
            $event.preventDefault();
        };

        // Получение списка просмотренного
        userList.get_dict_by_category(category).then(function (data) {
            $scope.user_list = data;
        });
	}
]);

/*
	Отображает описание продукта
*/
defaultApp.controller('DetailCtrl', ['$scope', '$http', '$location', 'oldLimits', 'workGenres',
	function ($scope, $http, $location, oldLimits, workGenres) {
        $scope.statuses = ['Add To List', 'Planned', 'Watch', 'ReWatching', 'Watched', 'Deffered', 'Dropped'];

        var id = $location.path().split('/')[2].split('-')[0];

        // Получение содержимого страницы
        $http.get('/api/products/id:' + id).success(function (data) {
            oldLimits.getRaiting_name_by_id(data.old_limit).then(function (limit) {
                data.old_limit = limit;
                $scope.product = data;
            });
        });

        // Показываем/скрываем форму
		$scope.add_form = function () {
			$scope.add_form_visible = !$scope.add_form_visible;
		};

        // Показываем форму
        $scope.show_editing = function (product) {
            $scope.add_form_visible = !$scope.add_form_visible;
            $scope.editing_product = true;
            workGenres.get_genre_objects_by_ids(product.genres_list.map(function (item) {
                return item.id;
            }), product.category).then(function (data) {
                product.genres = data;
            });
            $scope.product = product;
        };

    }
]);


defaultApp.controller('SeriesController', ['$http', '$scope', 'authProvider',
    function ($http, $scope, authProvider) {
        $scope.token = authProvider.getTokenValue();
        var id = window.location.pathname.split('/')[2].split('-')[0];

        $http.get('/api/seasons?product=' + id).success(function (data) {
            $scope.seasons = data.results;
            var count = 0;
            data.results.map(function (season) {
                return season.series.map(function (serie) {
                    count++;
                    if (!serie.length)
                        serie.length = " ";
                    if (serie.start_date)
                        serie.start_date = serie.start_date.slice(0, 10);
                    return serie;
                });
            });
            $scope.count_series = count;
        });

        // Создание нового сезона
        if ($scope.token) {
            $scope.create_season = function () {
                $http({
                    method: "POST",
                    url: "/api/seasons",
                    data: "product=" + id,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': authProvider.getToken()
                    }
                }).success(function (data) {
                    $scope.seasons.unshift(data);
                });
            };
        }

        $scope.serie_mouse_enter = function (serie) {
			serie.edit = true;
		};

		$scope.serie_mouse_leave = function (serie) {
			serie.edit = false;
		};

		$scope.show_menu = function (serie) {
			serie.menu = !serie.menu;
		};

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
		};

        $scope.edit_serie = function (serie) {};

        $scope.add_to_list_serie = function (serie) {
            $http({
                method: "POST",
                url: "/api/serielist",
                data: "serie=" + serie.id + "&product=" + id,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': authProvider.getToken()
                }
            }).success(function (data) {
                $scope.readed_series++;
                $scope.serielist['' + data.serie] = data;
            });
        };

        $scope.del_from_list_serie = function (serie, serielist) {
            $http({
                method: "DELETE",
                url: "/api/serielist/serie:" + serie.id,
                data: "",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': authProvider.getToken()
                }
            }).success(function () {
                delete serielist[serie.id];
                $scope.readed_series--;
            });
        };

        $scope.show_editing = function (serie) {
            serie.new_version = {number: serie.number, name: serie.name, start_date: serie.start_date, length: serie.length};
            serie.editing = !serie.editing;
        };

        $http.get('/api/serielist?user=' + localStorage.username + '&product=' + id, {headers: {
            'Authorization': authProvider.getToken()
        }}).success(function (data) {
            $scope.readed_series = data.count;
            $scope.readed_series_old = data.count;
            var tmp = {};
            for (var i in data.results)
                tmp['' + data.results[i]['serie']] = data;
            $scope.serielist = tmp;
        });

        // Редактирование серии
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
                serie.number = data.number;
                serie.name = data.name;
                serie.start_date = data.start_date.slice(0, 10);
                serie['length'] = serie.new_version['length'];
                serie.new_version = None;
            });
        };
	}
]);

defaultApp.controller('ProfileController', ['$scope', '$http', '$window',
    function ($scope, $http, $window) {
        $http.get('/api/profile', {headers: {
            'Authorization': 'Token ' + $window.localStorage.token
        }}).success(function (data) {
            $scope.user_list = data;
        });
    }]);

defaultApp.controller('UserCtrl', ['$scope', '$http', '$window',
    function ($scope, $http, $window) {
        $scope.statuses = ['', 'Planned', 'Watch', 'ReWatching', 'Watched', 'Deffered', 'Dropped'];
        $scope.statuses_lower = ['', 'planned', 'watch', 'rewatching', 'watched', 'deffered', 'dropped'];
        var arr = window.location.pathname.split('/');
        var category = arr[3];
        var status = $scope.statuses_lower.indexOf(arr[4]);

        var categories = JSON.parse($window.localStorage['categories']);
        for (var i in categories)
            if (categories[i].url == category)
                category = categories[i].id;

        $http.get('/api/userlist?status=' + status + '&category=' + category, {headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + localStorage.token
        }}).success(function (data) {
            $scope.user_list = data.results;
        });

        $scope.status_move = function (product, status) {};
    }]);


defaultApp.controller('CreatorController', ['$scope', 'FileUploader', '$http',
    function ($scope, FileUploader, $http) {
        $scope.add_form_visible = false;
        $scope.uploader = new FileUploader();
        var id = window.location.pathname.split('/')[2].split('-')[0];

        $scope.add_form = function () {
            $scope.add_form_visible = !$scope.add_form_visible;
        };

        $http.get('/api/serielist?user=' + localStorage.username + '&product=' + id, {headers: {
            'Authorization': 'Token ' + $scope.token
        }}).success(function (data) {
            console.log(data);
            $scope.readed_series = data.count;
            $scope.readed_series_old = data.count;
            var tmp = {};
            for (var i in data.results)
                tmp['' + data.results[i]['serie']] = data;
            $scope.serielist = tmp;
        });

        $scope.remove_image = function () {
            $scope.uploader.removeFromQueue(0);
        };

        $http.get('/api/creators?product=' + id).success(function (data) {
            $scope.creators = data.results;
        });

        $http.get('/api/employs').success(function (data) {
            $scope.employers = data.results;
            $scope.employs = [];
        });

        $scope.select_creator = function (creator) {
            $scope.searched_creator = creator;
            $scope.search_creator.name = creator.name;
            $scope.search_creators = [];
        };

        $scope.enter_creator_name = function () {
            if ($scope.search_creator.name.length > 1)
                $http.get('/api/search_creator?creator=' + $scope.search_creator.name).success(function (data) {
                    $scope.search_creators = data.results;
                });
            else {
                $scope.search_creators = [];
            }
        };

        $scope.filter_employs = function (employ) {
            $scope.employs = $scope.employers.filter(function (data) {
                return data.name.search('^.*' + employ + '.*', 'i') != -1;
            });
        };

        $scope.select_employ = function (employ) {
            $scope.creator.employ = employ.name;
            $scope.employs = [];
        };

        var product_url = window.location.pathname.split('/');
        product_url = product_url.slice(0, product_url.length - 2).join('/');

        $scope.statuses = ['Add To List', 'Planned', 'Watch', 'ReWatching', 'Watched', 'Deffered', 'Dropped'];

        $scope.add_creator = function () {
            // если мы заполнили нового персонажа
            if ($scope.creator.name) {
                $scope.creator.product = id;
                for (var i in $scope.employers)
                    if ($scope.employers[i].name == $scope.creator.employ)
                        $scope.creator.employ = $scope.employers[i].id;
                $scope.uploader.queue[0].alias = "avatar";
                $scope.uploader.onSuccessItem = function () {
                    $scope.add_form_visible = false;
                };
                $scope.uploader.queue[0].headers = {'Authorization': 'Token ' + window.localStorage.token};
                $scope.uploader.queue[0].formData.push($scope.creator);
                $scope.uploader.queue[0].url = "/api/creators";
                $scope.uploader.uploadAll();
//                window.location.pathname = window.location.pathname;
            } else {
                for (var i in  $scope.employers)
                    if ($scope.employers[i].name == $scope.creator.employ)
                        $scope.creator.employ = $scope.employers[i].id;
                $http({
                    method: "POST",
                    url: '/api/products/id:' + id + '/creators',
                    data: 'id=' + $scope.searched_creator.id + "&employ=" + $scope.creator.employ,
                    headers: {
                        'Authorization': 'Token ' + window.localStorage.token,
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                }).success(function (data) {
//                    window.location.pathname = window.location.pathname;
                });
            }
        };
    }]
);

defaultApp.controller('HeroController', ['$scope', 'FileUploader', '$http',
    function ($scope, FileUploader, $http) {
        var product_url = window.location.pathname.split('/');
        $scope.uploader = new FileUploader();

        $scope.add_form_visible = false;
        $scope.uploader = new FileUploader();
        var id = window.location.pathname.split('/')[2].split('-')[0];

        $scope.add_form = function () {
            $scope.add_form_visible = !$scope.add_form_visible;
        };

        $scope.remove_image = function () {
            $scope.uploader.removeFromQueue(0);
        };

        $http.get('/api/serielist?user=' + localStorage.username + '&product=' + id, {headers: {
            'Authorization': 'Token ' + $scope.token
        }}).success(function (data) {
//            console.log(data);
            $scope.readed_series = data.count;
            $scope.readed_series_old = data.count;
            var tmp = {};
            for (var i in data.results)
                tmp['' + data.results[i]['serie']] = data;
            $scope.serielist = tmp;
        });

        $scope.select_actor = function (h) {
            $scope.hero.actor = h.id;
            $scope.actors = [];
            $scope.hero.actor_name = h.name;
        };

        $scope.change_hero = function (hero_name) {
            // поиск имени "героя"
//            if (hero_name.length > 1) {
//                $http.get('/api/search_hero?hero=' + hero_name).success(function (data) {
//                    $scope.heroes = data.results;
//                });
//            } else {
//                $scope.heroes = [];
//            }
        };

        $scope.change_actor = function (actor_name) {
            if (actor_name.length > 1) {
                $http.get('/api/search_creator?creator=' + actor_name).success(function (data) {
                    $scope.actors = data.results;
                });
            } else {
                $scope.actors = [];
            }
        };

        $http.get('/api/heroes?product=' + id).success(function (data) {
            $scope.heroes = data.results;
        });
        $scope.statuses = ['Add To List', 'Planned', 'Watch', 'ReWatching', 'Watched', 'Deffered', 'Dropped'];

        $scope.submit_hero = function () {
            $scope.hero.product = id;
            $scope.hero.actors = $scope.hero.actor;
            console.log($scope.hero);
            $scope.uploader.queue[0].alias = "avatar";
            $scope.uploader.onSuccessItem = function () {
//                window.location.pathname = window.location.pathname;
            };
            $scope.uploader.queue[0].headers = {'Authorization': 'Token ' + window.localStorage.token};
            $scope.uploader.queue[0].formData.push($scope.hero);
            $scope.uploader.queue[0].url = "/api/heroes";
            $scope.uploader.uploadAll();
        }
    }]);


defaultApp.controller('SingleCreatorController', ['$scope', '$http', '$window',
    function ($scope, $http, $window) {
        var id = $window.location.pathname.split('/')[2].split('-')[0];
        $http.get('/api/creators/id:' + id).success(function (data) {
            $scope.creator = data;
        });
    }
]);


defaultApp.controller('SingleHeroController', ['$scope', '$http', '$window',
    function ($scope, $http, $window) {
        var id = $window.location.pathname.split('/')[2].split('-')[0];
        $http.get('/api/heroes/id:' + id).success(function (data) {
            $scope.hero = data;
        });
    }
]);

defaultApp.controller('addProductCtrl', ['$scope', 'oldLimits', 'FileUploader', 'workGenres', 'workCategories', 'authProvider', '$location',
    function ($scope, oldLimits, FileUploader, workGenres, workCategories, authProvider, $location) {
        $scope.uploader = new FileUploader();
        $scope.uploader.queueLimit = 1;

        oldLimits.getRaiting().success(function (data) {
            $scope.raiting = data.results;
        });

        var category = workCategories.getCategoryId(workCategories.getCategoryNameByUrl());

        workGenres.get_genre_list_by_category(category).then(function (data) {
            $scope.genres = data;
        });

        $scope.remove_image = function () {
			$scope.uploader.removeFromQueue(0);
		};

        $scope.select_genres = function (genre) {
            if (genre.length > 1) {
                $scope.search_genres = $scope.genres.filter(function (item) {
                    return item.name.indexOf(genre) != -1;
                });
            } else {
                $scope.search_genres = [];
            }
        };

        $scope.click_genre = function (genre) {
            if (!$scope.product)
                $scope.product = {};
            if (!$scope.product.genres)
                $scope.product.genres = [];
            $scope.genres.every(function (element) {
                if (element.name != genre.name)
                    return true;
                $scope.product.genres.push(element);
                $scope.search_genres = [];
                $scope.s_genre = '';
                return false;
            });
        };

        $scope.add_product = function () {
			$scope.product['category'] = category;
            $scope.uploader.onSuccessItem = function (data) {
                $location.path(data.url);
            };
            $scope.uploader.onErrorItem = function (data) {
                console.log(data);
            };
            $scope.product['genres'] = $scope.product['genres'].map(function (item) {
                return item.id;
            });
            $scope.product['old_limit'] = Number.parseInt($scope.product.old_limit);
            if ($scope.editing_product) {
                $scope.uploader.queue[0].method = "PUT";
                $scope.uploader.queue[0].url = '/api/products/id:' + $scope.product.id;
            } else {
			    $scope.uploader.queue[0].url = "/api/products";
            }
			$scope.uploader.queue[0].alias = "avatar";
            $scope.uploader.queue[0].headers = {'Authorization': authProvider.getToken()};
			$scope.uploader.queue[0].formData.push({'data': JSON.stringify($scope.product)});
			$scope.uploader.uploadAll();
		};
    }
]);

anylistApp.controller('OptionsCtrl', ['$scope', '$http', '$location', 'userList', 'urlFilters', 'authProvider',
    function ($scope, $http, $location, userList, urlFilters, authProvider) {
        var url = urlFilters.get_product_pathname($location.path());
        $scope.statuses = ['', 'Planned', 'Watch', 'ReWatching', 'Watched', 'Deffered', 'Dropped'];

        userList.get_object_by_product_id(urlFilters.get_product_id_by_url($location.path())).then(function (data) {
            $scope.readed_series = data.series;
            $scope.series_count = data.product.series_count;
            $scope.active_status = $scope.statuses[data.status];
        });
        $scope.contents = [
            {'name': 'Description', 'url': url},
            {'name': 'Series', 'url': url + '/series'},
            {'name': 'Heroes', 'url': url + '/heroes'},
            {'name': 'Creators', 'url': url + '/creators'}
        ];

        var id = urlFilters.get_product_id_by_url($location.path());

        $scope.status_move = function (status, active_status) {
            if (authProvider.getTokenValue() && status != active_status && status.length > 0) {
                var method = 'POST';
                if (active_status)
                    method = 'PUT';
                console.log(method);
                $http({
                    method: method,
                    url: "/api/userlist/product:" + id,
                    data: "name=" + status,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': authProvider.getToken()
                    }
                }).success(function () {
                    active_status = status;
                });
            } else if (status.length == 0) {
                status = active_status;
            }
        };

        $scope.change = function (series) {
            $scope.readed_series = series;
        };

        $scope.change_num_series = function (series) {
            $http({
                method: 'PUT',
                url: '/api/serielist/product:' + id + '/count',
                data: 'series=' + $scope.readed_series,
                headers: {
                    'Authorization': authProvider.getToken(),
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
        };
    }
]);