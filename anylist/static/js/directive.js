anylistApp.directive('ngThumb', ['$window', function($window) {
        var helper = {
            support: !!($window.FileReader && $window.CanvasRenderingContext2D),
            isFile: function(item) {
                return angular.isObject(item) && item instanceof $window.File;
            },
            isImage: function(file) {
                var type = '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
            }
        };

        return {
            restrict: 'A',
            template: '<canvas/>',
            link: function(scope, element, attributes) {
                if (!helper.support) return;

                var params = scope.$eval(attributes.ngThumb);

                if (!helper.isFile(params.file)) return;
                if (!helper.isImage(params.file)) return;

                var canvas = element.find('canvas');
                var reader = new FileReader();

                reader.onload = onLoadFile;
                reader.readAsDataURL(params.file);

                function onLoadFile(event) {
                    var img = new Image();
                    img.onload = onLoadImage;
                    img.src = event.target.result;
                }

                function onLoadImage() {
                    var width = params.width || this.width / this.height * params.height;
                    var height = params.height || this.height / this.width * params.width;
                    canvas.attr({ width: width, height: height });
                    canvas[0].getContext('2d').drawImage(this, 0, 0, width, height);
                }
            }
        };
}]);

// Проверяет, существует ли продукт с полностью совпадающим именем
// и если да, то выводит сообщение об ошибке
anylistApp.directive('noUnique', ['appSearch', function (appSearch) {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function (noUnique) {
                appSearch.search_product_by_title(noUnique).then(function (data) {
                    if (data) {
                        ctrl.$setValidity('noUnique', false);
                        noUnique = 'Production with this name already exists';
                        if (!scope.product)
                            scope.product = {};
                        scope.product.title = noUnique;
                        return noUnique;
                    } else {
                        ctrl.$setValidity('noUnique', true);
                        return undefined;
                    }
                });
            });
        }
    }
}]);

anylistApp.directive('productForm', [
    function () {
        return {
            restrict: 'E',
            templateUrl: 'productForm.html',
            replace: true,
            link: function (scope) {
            }
        }
    }
]);

anylistApp.directive('panel', [
    function () {
        return {
            restrict: 'E',
            templateUrl: 'panel.html',
            replace: true
        }
    }
]);

anylistApp.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keypress", function (event) {
            if (event.which === 13)
                scope.$apply(function () {
                    scope.$eval(attrs.ngEnter);
                });
        });
    }
});

anylistApp.directive('creatorForm', [
    function () {
        return {
            restrict: 'E',
            templateUrl: 'creatorForm.html',
            replace: true
        }
    }
]);