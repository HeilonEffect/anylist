anylistApp.factory('appSearch', ['$http', '$q',
    function ($http, $q) {
        var service = {};

        service.search_product_by_title = function (title) {
            var deferred = $q.defer();
            $http.get('/api/search?product=' + title).success(function (data) {
                if (data.results.length == 1 && data.results[0].name == title) {
                    deferred.resolve(true);
                } else
                    deferred.resolve(false);
            });
            return deferred.promise;
        };

        // Получение списка произведений с похожим названием
        service.get_products_by_title = function (title) {
            var deferred = $q.defer();
            if (title.length > 1)
                $http.get('/api/search?product=' + title).success(function (data) {
                    deferred.resolve(data.results);
                });
            else
                deferred.resolve([]);
            return deferred.promise;
        };

        return service;
    }
]);