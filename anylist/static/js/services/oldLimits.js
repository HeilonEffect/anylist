/**
 * Created by ctulhu on 19.08.14.
 */
anylistApp.factory('oldLimits', ['$http', '$window', function ($http, $window) {
    var serivce = {};
    var raiting = [];
    var promise = $http.get('/api/raitings');

    serivce.getRaiting = function () {
        return promise;
    };

    return serivce;
}]);