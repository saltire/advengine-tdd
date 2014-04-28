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
	$scope.views = ['Rooms', 'Nouns', 'Variables', 'Words', 'Controls'];
	$scope.switchView = function(view) {
		$scope.currentView = view;
		$scope.viewTemplate = 'partials/' + view.toLowerCase();
	};
	$scope.switchView($scope.views[0]);
}]);

advApp.controller('LogicControl', ['$scope', function($scope) {
	$scope.stages = ['Before Game', 'Before Turn', 'During Turn', 'After Turn', 'After Game'];
	$scope.isControl = angular.isObject;
}]);
