/**
 * Created by ctulhu on 19.08.14.
 */
anylistApp.factory('userList', ['$http', '$q', 'authProvider',
    function ($http, $q, authProvider) {
        var service = {};
        var promise;
        var token_value = authProvider.getTokenValue();
        if (token_value && token_value != 'undefined')
            promise = $http.get('/api/userlist', {
                headers: {
                    'Authorization': authProvider.getToken()
                }
            });

        service.get_list_by_category = function (category_id) {
            var deferred = $q.defer();
            promise.success(function (data) {
                deferred.resolve(data.results.filter(function (item) {
                    return item.product.category == category_id;
                }));
            });
            return deferred.promise;
        };

        service.get_dict_by_category = function (category_id) {
            var deferred = $q.defer();

            promise.success(function (data) {
                var result = {};
                data.results.filter(function (item) {
                    return item.product.category == category_id;
                }).forEach(function (item) {
                    result['' + item.product.id] = item;
                });
                if (data.next)
                    $http.get(data.next, {
                        headers: {
                            'Authorization': authProvider.getToken()
                        }
                    }).success(function (data) {
                        data.results.filter(function (item) {
                            return item.product.category == category_id;
                            }).forEach(function (item) {
                                result['' + item.product.id] = item;
                            });
                        deferred.resolve(result);
                    });
            });
            return deferred.promise;
        };

        service.add_to_list = function (elem) {
            var deferred = $q.defer();
            if (token_value && token_value != 'undefined')
                $http.post('/api/userlist/product:' + elem.product.id, 'name=Planned', {headers: {
                    'Authorization': authProvider.getToken(),
                    'Content-Type': 'application/x-www-form-urlencoded'
                }}).success(function (data) {
                    deferred.resolve(data);
                });
            return deferred.promise;
        };


        service.get_object_by_product_id = function (id) {
            var deferred = $q.defer();

            promise.success(function (data) {
                data.results.every(function (item) {
                    if (item.product.id != id)
                        return true;
                    deferred.resolve(item);
                    return false;
                });
            });
            return deferred.promise;
        };

        return service;
    }
]);