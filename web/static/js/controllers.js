
var counter = 0;
function CanvasCtrl($scope, $log) {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');

    $scope.data = [];

    $scope.addData = function() {
        $scope.draw($scope.data);
    };

    $scope.draw = function(data) {

    };

    $scope.get_images = function(){
        return [];
    };

    $scope.drawImage = function(){
        var images = $scope.get_images();
        for(var i=0; images.length; i++){
            var img = null;
            context.drawImage(img,10,10);
        }
    };

     $scope.init = function(){
        context.globalAlpha = 1.0;
        context.beginPath();
        $scope.draw($scope.data);
    };


}

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