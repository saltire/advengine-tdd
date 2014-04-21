var advApp = angular.module('advApp', []);

advApp.controller('AdvControl', function($scope, $http) {
	$scope.game = 'starflight';
	
	$http.get('/gamedata/' + $scope.game).then(function(response) {
		console.log(response.data);
		$scope.nouns = response.data.nouns;
		$scope.rooms = response.data.rooms;
		$scope.vars = response.data.vars;
		$scope.words = response.data.words;
	});
});