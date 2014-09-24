var App = angular.module('App', ['ngResource']);

App.config(['$interpolateProvider', '$httpProvider', function($interpolateProvider, $httpProvider) {
  // New symbols to prevent interference with Django templating language
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');

  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]);

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
      var error = formGroup.find('.label.label-danger');
      if (error.length > 0 && !error.is(':empty')) {
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

App.directive('loading', function($http) {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      scope.isLoading = function() {
        return $http.pendingRequests.length > 0;
      };

      loader = $('#loader').clone();

      scope.$watch(scope.isLoading, function(v) {
        if (v) {
          element.append(loader.show());
        } else {
          $(element).find('#loader').remove();
        }
      });
    }
  };
});

App.factory('Choropleth', ['$resource', function($resource) {
  return $resource('/choropleths/api/:id/ ', { id: '@id' }, {
    update: {
      method: 'PUT'
    }
  });
}]);

// Resource for Dataset
App.factory('Dataset', ['$resource', function($resource) {
  return $resource('/datasets/api/:id/ ');
}]);

// Resource for Palettes
App.factory('Palettes', ['$resource', function($resource) {
  return $resource('/choropleths/api/palettes/:id/ ');
}]);


App.controller('DatasetTableController', ['$scope', '$http', 'Dataset', function($scope, $http, Dataset) {

  $scope.init = function(id) {
    Dataset.get({id: id}, function(data) {
      $scope.dataset = data;
    });

    $scope.reverse = false;
    $scope.sortOrder='name';
  };
  
}]);

App.directive('progressBar', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      console.log(attrs);
      $(element).width(attrs.progressBar);
    }
  };
});

