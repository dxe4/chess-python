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

        var drawImage = function (imageObj, _x, _y) {
            var img = new Kinetic.Image({
                image: imageObj,
                x: _x,
                y: _y,
                width: imageObj.width,
                height: imageObj.height,
                name: imageObj.name,
                draggable: true
            });

            img.on('mouseover', function () {
                document.body.style.cursor = 'pointer';
            });
            img.on('mouseout', function () {
                document.body.style.cursor = 'default';
            });
            $log.info(img);
            $scope.layer.add(img);
        };

        function create_image(item, x, y) {
            var img = new Image();
            img.x = x;
            img.y = y;
            img.name = item;
            img.onload = function () {
                drawImage(this, x, y);
            };
            img.src = "static/img/" + item + ".png";
            return img;
        }

        $scope._init_images = function (data) {
            var x = 0;
            var y = 0;
            _.each(data, function (item) {
                if (item) {
                    var img = create_image(item, x, y);
                    images.push(img);
                }
                if (x >= piece_size * 8) {
                    x = 0;
                    y += piece_size;
                } else {
                    x += piece_size;
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
            $scope.stage = new Kinetic.Stage({
                container: "container",
                width: board_size,
                height: board_size
            });
            $scope.layer = new Kinetic.Layer();
            $scope._init();
            $scope.stage.add($scope.layer);
        };


    }]);


myApp.controller('TestCtrl', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {
        //use only for testing
    }]);

