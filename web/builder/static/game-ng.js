// create module
var advApp = angular.module('advApp', ['ngRoute']);

// some values
advApp.constant('game', 'starflight');
advApp.constant('views', {
	rooms: 'Rooms',
	nouns: 'Nouns',
	vars: 'Variables',
	words: 'Words',
	messages: 'Messages',
	controls: 'Controls'
});
advApp.value('gamedata', {});

advApp.config(['$routeProvider', 'views', function($routeProvider, views) {
	$routeProvider.when('/', {
		template: 'Welcome!',
		controller: 'homeController'
	});
	
	// map nav views to templates/controllers
	for (view in views) {
		$routeProvider.when('/' + view, {
			templateUrl: 'partials/' + view,
			controller: view + 'Controller'
		});
	}
}]);

advApp.controller('advController', ['$scope', '$location', '$http', 'game', 'views',
                                 function($scope, $location, $http, game, views) {
	// fetch game data
	$http.get('/gamedata/' + game).then(function(response) {
		$scope.game = response.data;
	});

	// values for nav menu
	$scope.nav = ['rooms', 'nouns', 'vars', 'words', 'messages', 'controls'];
	$scope.vnames = views;
	
	$scope.current = function() {
		return $location.path().slice(1);
	}
}]);

advApp.controller('homeController', ['$scope', function($scope) {
}]);

advApp.controller('roomsController', ['$scope', function($scope) {
	var roomList = $scope.$parent.game.rooms;
	var rooms = {};
	
	$scope.startRoom = '';
	for (i in roomList) {
		var room = roomList[i];
		
		rooms[room.id] = room;
		
		// find first room with start flag set to true
		if ($scope.startRoom == '' && room.is_start) {
			$scope.startRoom = room.id;
		}
	}
	
	$scope.getLabel = function(rid) {
		return rooms[rid].name || rooms[rid].id;
	}
}]);

advApp.controller('nounsController', ['$scope', function($scope) {
}]);

advApp.controller('varsController', ['$scope', function($scope) {
}]);

advApp.controller('wordsController', ['$scope', function($scope) {
}]);

advApp.controller('controlsController', ['$scope', function($scope) {
	$scope.stages = ['Before Game', 'Before Turn', 'During Turn', 'After Turn', 'After Game'];
	$scope.isControl = angular.isObject;
}]);

advApp.controller('messagesController', ['$scope', function($scope) {
}]);

