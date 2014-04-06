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