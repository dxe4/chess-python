var underscore = angular.module('underscore', []);
underscore.factory('_', function () {
    return window._;
});

var kinetic = angular.module('kinetic', []);
underscore.factory('kinetic', function () {
    return window.kinetic;
});

var myApp = angular.module('chess', ["underscore"]);
var image_type = ".png";


myApp.controller('CanvasCtrl', ['$scope', '$log', '$http', '_', 'kinetic',
    function ($scope, $log, $http, _, kinetic) {

        var canvas = document.getElementById('canvas');
        var context = canvas.getContext('2d');

        var piece_size = 80;
        var board_size = piece_size * 8;

        var white_pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP'];
        var black_pieces = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP'];

        $scope.data = null;
        $scope.killed = null;
        $scope.moves = null;

        $scope.addData = function () {
            //$scope.draw($scope.data);
        };

        $scope.draw = function (data) {
            var images = $scope.get_images();
            angular.forEach(images,
                function (value, key) {
                    // TODO add the real values here
                    $scope.drawImage(value, key, 0);
                }
            );
        };

        $scope.get_images = function () {
            return document.getElementById("piece_images").children;
        };

        $scope.drawImage = function (image, x, y) {
            $log.info(image);
            image.onload = function () {
                context.drawImage(image, x * piece_size, y * piece_size, image.width, image.height);
            };

        };

        $scope.resize_canvas = function () {
            canvas.width = board_size;
            canvas.height = board_size;
        };

        $scope._init = function () {
            $scope.resize_canvas();
            $http({method: 'GET', url: '/api/initial_board'}).
                success(function (data, status, headers, config) {
                    $scope.data = data["values"];
                });
        };

        $scope.init = function () {
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

