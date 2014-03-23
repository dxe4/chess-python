var image_type = ".png";
var chess = angular.module('chess');
chess.controller('CanvasCtrl', ['$scope', '$log', '$http','$cookies','$rootScope', '_', 'kinetic', 'LoginService',
    function ($scope, $log, $http,$cookies,$rootScope, _, kinetic, LoginService) {

        var piece_size = 80;
        var board_size = piece_size * 8;
        var images = [];
        var initial_board = [
            "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR",
            "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
            null, null, null, null, null, null, null, null, null,
            null, null, null, null, null, null, null, null, null,
            null, null, null, null, null, null, null, null, null,
            null, null, null, null, null,
            "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
            "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"
        ];

        $scope.data = null;
        $scope.killed = null;
        $scope.moves = null;
        $scope.current_image_values = null;

        var drawImage = function (imageObj, _x, _y, callback) {
            var current_pos = {x: _x, y: _y};
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

            img.on('dragstart', function (event) {
                //TODO make sure the piece to move is included in the valid moves
            });

            img.on('dragend', function (event) {
                //TODO send all valid moves from server after every move
                var valid = false;
                if (valid) {
                    current_pos = {x: img.x(), y: img.y()};
                    //TODO need to center in square;
                } else {
                    //TODO notify the user move was invalid...
                    //TODO if mouse gets out of the page, piece doesnt go back
                    img.setPosition(current_pos);
                    $scope.layer.draw();
                }
            });

            $scope.layer.add(img);
            if (callback) {
                callback();
            }
        };

        function create_image(item, x, y, callback) {
            var img = new Image();
            img.x = x;
            img.y = y;
            img.name = item;
            img.onload = function () {
                drawImage(this, x, y, callback);
            };
            img.src = "static/img/" + item + image_type;
            return img;
        }

        $scope._init_images = function (data) {
            var x = 0;
            var y = 0;

            var process_data = function (item, callback) {
                if (item) {
                    var img = create_image(item, x, y, callback);
                    images.push(img);
                }
                if (x >= piece_size * 7) {
                    x = 0;
                    y += piece_size;
                } else {
                    x += piece_size;
                }
            };
            var callback = _.after(31, function () {
                $scope.stage.add($scope.layer);
                var checkExists = setInterval(function () {
                    var _canvas = document.querySelector("#container canvas");
                    if (document.querySelector("#container canvas")) {
                        _canvas.style.backgroundImage = 'url(static/img/chessboard.png)';
                        clearInterval(checkExists);
                    }
                }, 100);
            });
            _.each(data, function (item) {
                process_data(item, callback);
            });

        };

        $scope.get_initial_data = function (move, callback) {

            $scope.data = initial_board;
            if (callback) {
                callback();
            }
//            $http({method: 'GET', url: '/api/initial_board'}).
//                success(function (data, status, headers, config) {
//                    $scope.data = data["values"];
//                    if (callback) {
//                        callback();
//                    }
//                });
        };

        $scope.startSSE = function () {
            if (!$scope.sse) {
                $scope.sse = new EventSource('/stream');
                $scope.sse.onmessage = function (message) {
                    $log.info(message.data);
                    var _json = angular.fromJson(message.data);
                    $log.info(_json);
                    $log.info(_json["count"]);
                    $log.info(_json["message"]);
                    if (_json.count === 3) {
                        $scope.sse.close();
                        $scope.sse = null;
                    }
                };
            }
        };

        $scope.startClicked = function () {
            $scope.startSSE();
        };

        $scope.login = function (_username) {
            LoginService.login(_username);
        };

        $scope.logout = function(){
            LoginService.logout();
        };

        $scope._init = function () {
            var callback = _.after(1, function () {
                $scope._init_images($scope.data);
            });
            $scope.get_initial_data(null, callback);
        };

        $scope.init = function () {
            if ($cookies.username){
                $rootScope.logged_in = $cookies.username;
            }
            $scope.stage = new Kinetic.Stage({
                container: "container",
                width: board_size,
                height: board_size
            });
            $scope.layer = new Kinetic.Layer();
            $scope._init();
        };

        $scope.dropdown_clicked = function (e) {
            e.preventDefault();
            e.stopPropagation();
        };

    }]);


//myApp.controller('TestCtrl', ['$scope', '$log', '$http',
//    function ($scope, $log, $http) {
//        //use only for testing
//    }]);

