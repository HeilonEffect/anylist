/**
 * Created by ctulhu on 19.08.14.
 */
anylistApp.factory('workCategories', ['$http', '$location', '$q',
    function ($http, $location, $q) {
        var service = {};
        var categories = {};
        var promise = $http.get('/api/categories/');

        service.getCategories = function () {
            var deferred = $q.defer();

            promise.success(function (data) {
                deferred.resolve(data.results);
            });
            return deferred.promise;
        };

        service.getCategoryId = function () {
            var deferred = $q.defer();

            promise.success(function (data) {
                var result = {};
                data.results.forEach(function (item) {
                    categories[item.name] = item.id;
                });
                deferred.resolve(result);
            });

            return deferred.promise;
        };

        service.getCategoryUrlById = function (id) {
            var deferred = $q.defer();

            promise.success(function (data) {
                data.results.every(function (item) {
                    if (item.id != id)
                        return true;
                    deferred.resolve(item.url);
                    return false;
                });
            });

            return deferred.promise;
        };

        service.getCategoryName = function (id) {
            var deferred = $q.defer();
            promise.success(function (data) {
                var result = {};
                data.results.forEach(function (item) {
                    result['' + item.id] = item.name;
                });
                deferred.resolve(result[id]);
            });
            return deferred.promise;
        };

        service.getCategoryNameByUrl = function (url) {
            var deferred = $q.defer();

            promise.success(function (data) {
                if (url)
                    url = '/' + url;
                else
                    url = '/' + $location.path().split('/')[1];
                data.results.every(function (item) {
                    if (item.url != url)
                        return true;
                    deferred.resolve(item.name);
                    return false;
                });
            });
            return deferred.promise;
        };

        service.getCategoryIdByUrl = function (url) {
            var deferred = $q.defer();
            promise.success(function (data) {
                if (url)
                    url = '/' + url;
                else
                    url = '/' + $location.path().split('/')[1];
                data.results.every(function (item) {
                    if (item.url != url)
                        return true;
                    deferred.resolve(item.id);
                    return false;
                });
            });
            return deferred.promise;
        };

        service.getCategoryUrlByName = function (name) {
            return name.toLowerCase();
        };

        return service;
    }
]);
