var chess = angular.module('chess');
chess.controller('NavBarCtrl',
    function ($scope, $cookies, $rootScope, LoginService) {


        $scope.login = function (_username) {
            LoginService.login(_username);
        };

        $scope.logout = function(){
            LoginService.logout();
        };


        $scope.init = function () {
            if ($cookies.username){
                $rootScope.logged_in = $cookies.username;
            }
        };
        $scope.dropdown_clicked = function (e) {
            e.preventDefault();
            e.stopPropagation();
        };

    });


//myApp.controller('TestCtrl', ['$scope', '$log', '$http',
//    function ($scope, $log, $http) {
//        //use only for testing
//    }]);

