var App = angular.module('App', ['ngResource']);

App.config(['$interpolateProvider', '$httpProvider', function($interpolateProvider, $httpProvider) {
  // New symbols to prevent interference with Django templating language
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');

  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]);

// Browser detection messaging
App.directive('isFirefox', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      var KEY = 'texaschoropleth:firefox-message-dismiss';
      if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1) {
        if (localStorage.getItem(KEY)) {
          return;
        }

        var message = $(element);

        message.removeClass('hidden');
        message.on('close.bs.alert', function() {
          localStorage.setItem(KEY, 1);
        });
      }
    }
  };
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

// Directive for placing a popover on one element, 
// and triggering it with another
App.directive('targetedPopover', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      var timeout = 200;

      if ($(element).parent().attr('smooth-scroll') !== undefined) {
        timeout = timeout + 1000;
      }

      options = {
        content: attrs.content,
        placement: attrs.placement
      };

      var popover = $(attrs.targetedPopover);
      // Instantiate the popover
      popover.popover(options);

      $(element).on('click', function() {
        setTimeout(function() {
          popover.popover('show');
        }, timeout);

        setTimeout(function() {
          popover.popover('hide');
        }, 5000);
      });
    }
  };
});

// Smooth scroll to on page anchor tags
App.directive('smoothScroll', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      $(element).click(function(e) {
        e.preventDefault();

        var scroll = function(x) {
          $('html, body').animate({
            scrollTop: x
          }, 1000);
        };

        var target = $(attrs.href);
        if (target.length) {
          scroll(target.offset().top);

          // Return to the top of the page
          setTimeout(function() { scroll(0); }, 3000 );
          return false;
        }
      });
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

// Ajax loader
App.directive('loading', function($http) {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      var loader = $('#loader').clone();

      if (attrs.loading === 'http') {
          element.append(loader.show());
        return;
      }

      scope.isLoading = function() {
        return $http.pendingRequests.length > 0;
      };


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
  return $resource('/api/choropleths/:id/ ', { id: '@id' }, {
    update: {
      method: 'PUT'
    }
  });
}]);

// Resource for Dataset
App.factory('Dataset', ['$resource', function($resource) {
  return $resource('/api/datasets/:id/ ');
}]);

// Resource for Palettes
App.factory('Palettes', ['$resource', function($resource) {
  return $resource('/api/choropleths/palettes/:id/ ');
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
      $(element).width(attrs.progressBar);
    }
  };
});

