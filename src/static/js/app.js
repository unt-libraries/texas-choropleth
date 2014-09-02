var App = angular.module('App', ['ngResource']);

App.config(function($interpolateProvider, $httpProvider) {
    // New symbols to prevent interference with Django templating language
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
});

// Bootstrap active tab helper
App.directive('isActive', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            if (attrs.href === window.location.pathname) {
                element.parent().addClass('active');
            }
        }
    };
});

// Still uses the data-content attr for content
App.directive('popover', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            options = {
                trigger: 'hover'
            };
            $(element).popover(options);
        }
    };
});

// Form Validation helper
App.directive('hasError', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var formGroup = $(element);
            if (formGroup.find('.errorlist').length > 0) {
                formGroup.addClass('has-error');
            }
        }
    };
});

// Add a Bootstrap tooltip
App.directive('tooltip', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            $(element).tooltip();
        }
    };
});

// Helper for notifications and list-item-icons
App.directive('hasRecords', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            // Compare it with the python bool 
            if (attrs.records == 'False') {
                element.addClass('no-records');
            }
        }
    };
});


