var underscore = angular.module('underscore', []);
underscore.factory('_', function () {
    return window._;
});


var kinetic = angular.module('kinetic', []);
kinetic.factory('kinetic', function () {
    return window.kinetic;
});

var myApp = angular.module('chess', ["underscore", "kinetic"]);

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
                //context.drawImage(image, x * piece_size, y * piece_size, image.width, image.height);
            };

        };

        $scope.resize_canvas = function () {
            //TODO change this back to normal when done with kinetic
            canvas.width = board_size - 400;
            canvas.height = board_size - 400;
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

        function drawImage(imageObj) {
            var stage = new Kinetic.Stage({
                container: "container",
                width: 400,
                height: 400
            });
            var layer = new Kinetic.Layer();

            var img = new Kinetic.Image({
                image: imageObj,
                x: 0,
                y: 0,
                width: imageObj.width,
                height: imageObj.height,
                draggable: true
            });

            img.on('mouseover', function () {
                document.body.style.cursor = 'pointer';
            });
            img.on('mouseout', function () {
                document.body.style.cursor = 'default';
            });

            layer.add(img);
            stage.add(layer);
        }

        //var imageObj = $scope.get_images()[0];
        var imageObj = new Image();
        imageObj.onload = function () {
            drawImage(this);
        };
        imageObj.src = 'static/img/bK.png';

    }]);


myApp.controller('TestCtrl', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {
        //use only for testing
    }]);

