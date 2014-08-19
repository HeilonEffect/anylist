/**
 * Created by ctulhu on 19.08.14.
 */
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