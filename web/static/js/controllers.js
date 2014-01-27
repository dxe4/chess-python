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

        var piece_size = 80;
        var board_size = piece_size * 8;

        var images = [];

        $scope.data = null;
        $scope.killed = null;
        $scope.moves = null;

        $scope.resize_canvas = function () {
            //TODO change this back to normal when done with kinetic
            canvas.width = board_size - 400;
            canvas.height = board_size - 400;
        };

        $scope._init_images = function (data) {
            var x = 0;
            var y = 0;
            _.each(data, function (item) {
                if (item) {
                    var img = new Image();
                    img.x = x;
                    img.y = y;
                    img.onload = function () {
                        drawImage(this);
                    };
                    img.src = "static/img/" + item + ".png"
                    images.push(img);
                }
            });
        };

        $scope._init = function () {
            $http({method: 'GET', url: '/api/initial_board'}).
                success(function (data, status, headers, config) {
                    $scope.data = data["values"];
                    $log.info(data);
                    $scope._init_images($scope.data);
                });
        };

        $scope.init = function () {
            $scope._init();
        };

        function drawImage(imageObj) {
            var stage = new Kinetic.Stage({
                container: "container",
                width: board_size,
                height: board_size
            });
            var layer = new Kinetic.Layer();

            var img = new Kinetic.Image({
                image: imageObj,
                x: imageObj.x,
                y: imageObj.y,
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

    }]);


myApp.controller('TestCtrl', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {
        //use only for testing
    }]);

