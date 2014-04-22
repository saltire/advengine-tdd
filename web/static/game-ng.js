// create module
var advApp = angular.module('advApp', []);

// add a value
advApp.value('game', 'starflight');

advApp.controller('AdvControl', ['$scope', '$http', 'game', function($scope, $http, game) {
	// fetch game data
	$http.get('/gamedata/' + game).then(function(response) {
		$scope.game = response.data;
	});

	// set views, and allow us to switch
	$scope.views = ['rooms', 'nouns', 'vars', 'words', 'controls'];
	$scope.switchView = function(view) {
		$scope.currentView = view;
		$scope.viewTemplate = 'partials/' + view;
	};
	$scope.switchView($scope.views[0]);
}]);
