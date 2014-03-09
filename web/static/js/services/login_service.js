var chess = angular.module('chess');

chess.service('LoginService', function ($http, $rootScope, $log) {
        return {
            login: function (_username) {
                var _data = angular.toJson({ username: _username});
                $http({
                    method: 'POST',
                    url: "/login",
                    data: _data,
                    headers: { 'Content-Type': 'application/json' }
                }).success(function (data, status, headers, config) {
                        $rootScope.logged_in = data;
                    });
            }
        }
    });