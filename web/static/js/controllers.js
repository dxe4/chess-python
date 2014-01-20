var image_type = ".png";
function CanvasCtrl($scope, $log, $http) {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');

    var white_pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP'];
    var black_pieces = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP'];

    $scope.data = null;
    $scope.killed = null;
    $scope.moves = null;

    $scope.addData = function() {
        //$scope.draw($scope.data);
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

     $scope._init = function(){
         $http({method: 'GET', url: '/api/initial_board'}).
                success(function(data, status, headers, config) {
                    $scope.data = data["values"];
             });
     };

     $scope.init = function(){
        $scope._init();
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