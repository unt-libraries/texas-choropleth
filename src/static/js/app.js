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

// Choropleth Tour
App.directive('choroplethTour', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
        steps = [
          {
            element: '#map-controls',
            title: 'Map Controls',
            content: 'Use these controls to configure the look and feel. Click the <span class="glyphicon glyphicon-info-sign"></span> icon for more information on each form field.',
            placement: 'left'
          },
          {
            element: '#description-tab',
            title: 'Description',
            content: 'Use the text box below to add description of your choropleth and/or dataset. The description is Markdown-enabled. There is a link to the Markdown website and specification on the \'Cheatsheet\' tab. If you prefer not to use Markdown, then simply enter the plain text into the description box.',
            placement: 'top'
          },
          {
            element: '#save',
            title: 'Save',
            content: 'Once you are satisfied with your configuration,  click this \'Save\' to finish.',
            placement: 'left'
          }
        ];
      var tour = new Tour({name:'choropleth', steps:steps});
      tour.init();

      $(element).click(function() {
        localStorage.removeItem('choropleth_end');
        localStorage.removeItem('choropleth_current_step');
        tour.start();
      });
    }
  };
});

// Dataset Tour
App.directive('datasetTour', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
        steps = [
          {
            element: '#csv-template',
            title: 'Dataset Template',
            content: 'In order to upload your dataset, the dataset document must pass strict validation. We created this template so that all you have to do is put in the data for the corresponding county.',
            placement: 'right'
          },
          {
            element: '#datafile-form',
            title: 'Upload',
            content: 'Once your data has been added to the template, add your file to the form and click \'Upload\'.',
            placement: 'left'
          },
        ];
      var tour = new Tour({name: 'dataset', steps:steps});
      tour.init();

      $(element).click(function() {
        localStorage.removeItem('dataset_end');
        localStorage.removeItem('dataset_current_step');
        tour.start();
      });
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

