/**
 * Created by ctulhu on 19.08.14.
 */
anylistApp.factory('oldLimits', ['$http', '$q', function ($http, $q) {
    var serivce = {};
    var promise = $http.get('/api/raitings');

    serivce.getRaiting = function () {
        return promise;
    };

    serivce.getRaiting_id_by_name = function (name) {
        var deferred = $q.defer();
        promise.success(function (data) {
            data.results.every(function (elem) {
                if (elem.name != name)
                    return true;
                deferred.resolve(elem.id);
                return false;
            });
        });
        return deferred.promise;
    };

    serivce.getRaiting_name_by_id = function (id) {
        var deferred = $q.defer();
        promise.success(function (data) {
            data.results.every(function (elem) {
                if (elem.id != id)
                    return true;
                deferred.resolve(elem.name);
                return false;
            });
        });
        return deferred.promise;
    };

    return serivce;
}]);