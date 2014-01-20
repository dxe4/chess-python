function FooCtrl($scope,$log,$http) {

    $scope.foo = function () {
            $http({method: 'GET', url: '/foo'}).
                success(function(data, status, headers, config) {
                        $scope.bar = data["result"];
                }).
                error(function(data, status, headers, config) {
                });
    };

    $scope.init = function () {
        $scope.foo();
    };

}