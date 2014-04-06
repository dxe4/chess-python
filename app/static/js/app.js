'use strict';

var underscore = angular.module('underscore', []);
underscore.factory('_', function () {
    return window._;
});

var eventsource = angular.module('eventsource', []);
underscore.factory('eventsource', function () {
    return window.eventsource;
});

var kinetic = angular.module('kinetic', []);
kinetic.factory('kinetic', function () {
    return window.kinetic;
});

angular.module('chess', ["ngCookies", "underscore", "kinetic", "eventsource", "ui.bootstrap"]);
