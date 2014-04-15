var chess = angular.module('chess');

chess.service('SocketService', function ($http, $rootScope, $cookies, $log) {

    var _socket = null;
    var data = {
        "data": {
            "id": 12345679,
            "player": "foo"
        },
        "type": "join_queue"
    };

    return {
        openSocket: function () {
            if (_socket === null) {
                _socket = new WebSocket("ws://localhost:8081/ws/");
                console.log("init");
                _socket.onopen = function (evt) {
                    console.log(evt);
                    _socket.send(angular.toJson(data));
                };
                _socket.onclose = function (evt) {
                    console.log(evt);
                    _socket = null;
                };
                _socket.onmessage = function (evt) {
                    console.log(evt);
                    alert(evt.data);
                };
                _socket.onerror = function (evt) {
                    console.log(evt);
                    _socket = null;
                };
            } else {
                _socket.close();
            }
        }
    }
});