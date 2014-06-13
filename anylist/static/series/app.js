'use strict';

angular.module('series', ['series.services', 'series.filters'])
	.config(['$routeProvider', function($routeProvider) {
		$routeProvider
			.when('/series', {template: 'view/series.html', controller: SeriesCtrl})
			.otherwise({redirectTo: '/series'});
	},
]);