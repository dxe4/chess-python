var myApp = angular.module('chess', []);
var image_type = ".png";

myApp.controller('CanvasCtrl', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {

    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');

    var white_pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP'];
    var black_pieces = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP'];

    $scope.data = null;
    $scope.killed = null;
    $scope.moves = null;

    $scope.addData = function () {
        //$scope.draw($scope.data);
    };

    $scope.draw = function (data) {

    };

    $scope.get_images = function () {
        //return angular.element("#piece_images img");
        return [];
    };

    $scope.drawImage = function () {
        var images = $scope.get_images();
        for (var i = 0; images.length; i++) {
            var img = null;
            context.drawImage(img, 10, 10);
        }
    };

    $scope._init = function () {
        $http({method: 'GET', url: '/api/initial_board'}).
            success(function (data, status, headers, config) {
                $scope.data = data["values"];
            });
    };

    $scope.init = function () {
        $log.info($scope.get_images());
        $scope._init();
        context.globalAlpha = 1.0;
        context.beginPath();
        $scope.draw($scope.data);
    };
}]);


myApp.controller('TestCtrl', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {
    //use only for testing
}]);
