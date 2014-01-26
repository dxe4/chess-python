var myApp = angular.module('chess', []);
var image_type = ".png";



myApp.controller('CanvasCtrl', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {

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

        $scope.draw_board = function () {
            context.fillStyle = "rgba(130, 110, 50, 0.5)";
            for (var i = 0; i < 8; i++) {
                for (var j = 0; j < 8; j++) {
                    context.moveTo(0, piece_size * j);
                    context.lineTo(board_size, piece_size * j);
                    context.stroke();
                    context.moveTo(piece_size * i, 0);
                    context.lineTo(piece_size * i, board_size);
                    context.stroke();
                    var left = 0;
                    for (var a = 0; a < 8; a++) {
                        for (var b = 0; b < 8; b += 2) {
                            var startX = b * piece_size;
                            if (a % 2 == 0) startX = (b + 1) * piece_size;
                            context.fillRect(startX + left, (a * piece_size), piece_size, piece_size);
                        }
                    }
                }
            }
            context.fillStyle = "rgba(0, 0, 0)";
        };

        $scope.get_images = function () {
            return document.getElementById("piece_images").children;
        };

        $scope.drawImage = function (image, x, y) {
            $log.info(image);
            image.onload = function () {
                context.drawImage(image, x*piece_size, y*piece_size, image.width, image.height);
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
            $scope.draw_board();
        };
    }]);


myApp.controller('TestCtrl', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {
        //use only for testing
    }]);
