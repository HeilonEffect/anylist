/**
 * Created by ctulhu on 19.08.14.
 */
anylistApp.factory('workGenres', ['$http', '$q', function ($http, $q) {
    var service = {};
    var promise = $http.get('/api/genres');

    service.get_genres = function () {
        return promise;
    };

    service.get_genres_by_category = function (category) {
        var deferred = $q.defer();
        promise.success(function (data) {
            data = data.results.filter(function (item) {
                return item.categories.indexOf(category) != -1;
            });
            deferred.resolve(data);
        });
        return deferred.promise;
    };

    return service
}]);