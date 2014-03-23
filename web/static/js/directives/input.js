angular.module('chess')
    .directive('stop-propagation', function () {
        return {
            restrict: 'A',
            link: function (scope, element) {
                element.bind('click', function (event) {
                    event.stopPropagation();
                });
            }
        };
    });

angular.module('chess').directive('stop-propagation-2', function () {
    return {
        restrict: 'A',
        link: function (scope, element) {
            element.bind('hide.bs.dropdown', function (event) {
                console.log("0d0sa0d0as");
                return false;
            });
        }
    };
});