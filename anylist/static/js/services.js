anylistApp.factory('urlFilters', ['$location', function ($location) {
    var service = {};

    service.getFilters = function () {
        var filters = $location.path().split('/');
        var genres = [];
        var limits = [];
        var genres_position = filters.indexOf('genres');
        var old_limit_position = filters.indexOf('old_limit');
        var result = {};

        // Извлекаем фильтры из url
        if (genres_position != -1)
            genres = filters[genres_position + 1].split(',');
        if (old_limit_position != -1)
            limits = filters[old_limit_position + 1].split(',');

        // Создаём объект с нужными фильтрами
        result['genres'] = genres;
        result['old_limit'] = limits;
        return result;
    };

    /*
        Переходим на url, содержащий указанные фильтры
        Формат filters совпадает с форматом getFilters()
     */
    service.forward_by_filters = function (filters, category) {
        var result = '';
        for (var key in filters)
            if (filters[key].length > 0)
                result += '/' + key + '/' + filters[key].join(',');
        if (result.length > 0)
            result = '/filter' + result;
        $location.path('/' + category + result);
    };

    return service;
}]);

anylistApp.factory('workCategories', ['$http', '$window', function ($http, $window) {
    var service = {};
    var categories = {};
    var categories_ids = {};
    var categories_url = {};

    function getCategories() {
        if (!$window.localStorage.categories) {
            $http.get('/api/categories').success(function (data) {
                for (var i in data.results)
                    for (var j in data.results[i].categories) {
                        categories[data.results[i].categories[j].name] = data.results[i].categories[j].id;
                        categories_ids['' + data.results[i].categories.id] = data.results[i].categories[j].name;
                        categories_url['' + data.results[i].categories.url] = data.results[i].categories[j].name;
                    }
            });
            $window.localStorage.categories = JSON.stringify(result);
        } else {
            var result = $window.localStorage.categories;
            result = JSON.parse(result);
            for (var i in result) {
                categories[result[i].name] = result[i].id;
                categories_ids['' + result[i].id] = result[i].name;
                categories_url['' + result[i].url] = result[i].name;
            }
        }
    }
    getCategories();

    service.getCategoryId = function (name) {
        return categories[name];
    };

    service.getCategoryName = function (id) {
        return categories_ids[id];
    };

    service.getCategoryNameByUrl = function () {
        return categories_url[$window.location.pathname.split('/')[1]];
    };

    service.getCategoryUrlByName = function (name) {
        return name.toLowerCase();
    };

    return service;
}]);