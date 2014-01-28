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
        var board_size = piece_size * 9;

        var images = [];

        $scope.data = null;
        $scope.killed = null;
        $scope.moves = null;

        var drawImage = function (imageObj, _x, _y, f) {
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
            $scope.layer.add(img);
            f();
        };

        function create_image(item, x, y, f) {
            var img = new Image();
            img.x = x;
            img.y = y;
            img.name = item;
            img.onload = function () {
                drawImage(this, x, y, f);
            };
            img.src = "static/img/" + item + ".png";
            return img;
        }

        $scope._init_images = function (data) {
            var x = 0;
            var y = 0;

            var process_data = function (item, f) {
                if (item) {
                    var img = create_image(item, x, y, f);
                    images.push(img);
                }
                if (x >= piece_size * 7 ) {
                    x = 0;
                    y += piece_size;
                } else {
                    x += piece_size;
                }
            };
            var f = _.after(31, function (x) {
                $scope.stage.add($scope.layer);
            });
            _.each(data, function (item) {
                process_data(item, f);
            });

        };

        $scope._init = function () {
            $http({method: 'GET', url: '/api/initial_board'}).
                success(function (data, status, headers, config) {
                    $scope.data = data["values"];
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
        };


    }]);


myApp.controller('TestCtrl', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {
        //use only for testing
    }]);

