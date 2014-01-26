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
            var images = $scope.get_images();
            angular.forEach(images,
                function (value, key) {
                    if (key == 0) {
                        $scope.drawImage(value);
                    }

                }
            );
        };

        $scope.get_images = function () {
            return document.getElementById("piece_images").children;
        };

        $scope.drawImage = function (image) {
            $log.info(image);
            image.onload = function() {
                context.drawImage(image, 0, 0, image.width, image.height);
            };

        };

        $scope.resize_canvas = function(x, y) {
            canvas.width = x;
            canvas.height = y;
        };

        $scope._init = function () {
            $scope.resize_canvas(600, 600);
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
