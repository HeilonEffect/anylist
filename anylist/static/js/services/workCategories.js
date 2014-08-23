/**
 * Created by ctulhu on 19.08.14.
 */
anylistApp.factory('workCategories', ['$http', '$window', function ($http, $window) {
    var service = {};
    var categories = {};
    var categories_ids = {};
    var categories_url = {};
    var result;

    function loadCategories() {
        if (!$window.localStorage.categories && $window.localStorage['categories'] != 'undefined') {
            $http.get('/api/categories').success(function (data) {
                result = data;
                result.forEach(function (item) {
                    categories[item.name] = item.id;
                    categories_ids['' + item.id] = item.name;
                    categories_url['' + item.url] = item.name;
                });
            });
            $window.localStorage.categories = JSON.stringify(result);
        } else {
            result = $window.localStorage.categories;
            result = JSON.parse(result);
            result.forEach(function (item) {
                categories[item.name] = item.id;
                categories_ids['' + item.id] = item.name;
                categories_url['' + item.url] = item.name;
            });
        }
    }
    loadCategories();

    service.getCategories = function () {
        return result;
    };
    service.getCategoryId = function (name) {
        return categories[name];
    };

    service.getCategoryName = function (id) {
        return categories_ids[id];
    };

    service.getCategoryNameByUrl = function (url) {
        if (url)
            return categories_url['/' + url];
        return categories_url['/' + $window.location.pathname.split('/')[1]];
    };

    service.getCategoryUrlByName = function (name) {
        return name.toLowerCase();
    };

    return service;
}]);
