/**
 * Created by ctulhu on 19.08.14.
 */
anylistApp.factory('authProvider', ['$http', '$window', '$q',
    function ($http, $window, $q) {
        var service = {};

        // data = {'username': <String>, 'password': <String>}
        service.login = function (data) {
            var deferred = $q.defer();
            if (data.is_reg) {
                $http.post('/register', data, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).success(function (token) {
                    deferred.resolve({'username': token['username'], 'token': token['token']});
                    $window.localStorage['token'] = token['token'];
                    $window.localStorage['username'] = data['username'];
                });
            } else {
                $http.post('/api-token-auth/', data, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).success(function (token) {
                    deferred.resolve({'username': token['username'], 'token': token['token']});
                    $window.localStorage['token'] = token['token'];
                    $window.localStorage['username'] = data['username'];
                });
            }
            return deferred.promise;
        };

        service.logout = function () {
            $window.localStorage.removeItem('token');
            $window.localStorage.removeItem('username');
        };

        service.getTokenValue = function () {
            return $window.localStorage['token'];
        };

        service.getToken = function () {
            var token = $window.localStorage['token'];
            if (token && token != 'undefined')
                return 'Token ' + token;
            return undefined;
        };

        service.getUsername = function () {
            var username = $window.localStorage['username'];
            if (username && username != 'undefined')
                return username;
            return undefined;
        };
        return service;
    }
]);