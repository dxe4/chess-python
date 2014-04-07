var chess = angular.module('chess');
chess.controller('NavBarCtrl',
    function ($scope, $cookies, $rootScope, $log, $modal, UserService) {

        var ModalInstanceCtrl = function ($scope, $modalInstance, sign_up) {

            var constructor = function () {
                if (sign_up) {
                    $scope.modal_title = "Sign Up!";
                } else {
                    $scope.modal_title = "Sign In!";
                }
            };
            constructor();

            $modalInstance.result.then(function () {
            }, function () {
            });

            $scope._close = function () {
                $modalInstance.close();
            };

            $scope.login = function (username) {
                UserService.login(username);
                $modalInstance.close();
            };

            $scope.register = function (data) {

            };

        };

        var popUp = function (_sign_up) {
            $modal.open({
                templateUrl: 'static/templates/modal.html',
                controller: ModalInstanceCtrl,
                resolve: {
                    sign_up: function () {
                        return _sign_up;
                    }
                }
            });
        };

        $scope.logout = function () {
            UserService.logout();
        };


        $scope.init = function () {
            console.log($cookies.username);
            if ($cookies.username) {
                $rootScope.logged_in = $cookies.username;
            }
        };

        $scope.sign_in_clicked = function () {
            popUp(false);
        };

        $scope.sign_up_clicked = function () {
            popUp(true);
        };

    });
