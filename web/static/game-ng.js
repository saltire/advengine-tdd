// create module
var advApp = angular.module('advApp', ['ngRoute']);

// add a value
advApp.value('game', 'starflight');

advApp.controller('AdvControl', ['$scope', '$http', 'game', function($scope, $http, game) {
	// fetch game data
	$http.get('/gamedata/' + game).then(function(response) {
		$scope.rooms = response.data.rooms;
		$scope.nouns = response.data.nouns;
		$scope.vars = response.data.vars;
		$scope.words = response.data.words;
	});

	// set views, and allow us to switch
	$scope.views = ['rooms', 'nouns', 'vars', 'words'];
	$scope.switchView = function(view) {
		$scope.currentView = view;
		$scope.viewTemplate = 'partials/' + view;
	};
	$scope.switchView($scope.views[0]);
}]);
