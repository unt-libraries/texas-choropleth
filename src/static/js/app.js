var App = angular.module('App', []);

App.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
})

// Still uses the data-content attr for content
App.directive('popover', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            options = {
                trigger: 'hover'
            }
            $(element).popover(options);
        }
    }
});

App.directive('hasError', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var formGroup = $(element);
            if (formGroup.find('.errorlist').length > 0) {
                formGroup.addClass('has-error');
            }
        }
    }
});
