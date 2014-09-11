App.directive('choropleth', function($window) {

  var loader = $("#loader").clone();
  var hasLoader = loader.length > 0;


  if (hasLoader) {
      var choropleth = $("#choropleth");
          choropleth.append(loader.show());
  }

  var width = 600,
      height = 600;

  // D3 Array Object where the data is stored as key : value
  var rateById = d3.map();

  // Projection for Map
  var projection = d3.geo.transverseMercator()
      .rotate([100 + 20 / 60, -29 - 40 / 60])
      .scale(3000)
      .translate([285, 380]);

  // Declare the path object
  var path = d3.geo.path()
        .projection(projection);

  return {
    restrict: "E",
    scope: {
      data: '=',
      domain: '=',
      range: '=',
      label: '=',
      scheme: '=',
      scale: '=',
      palette: '=',
    },
    link: function (scope, element, attrs) {
      var scale, svg, $svg;

      svg = d3.select(element[0]).append("svg")
        .attr("width", width)
        .attr("height", height);

      $svg = $('svg');

      hasLoader ? $svg.hide() : false;

      // Watch for changes in the dataset
      scope.$watch('data', function(newVals, oldVals) {
        updateData(newVals);
      }, true);

      scope.$watchCollection('[scale, range, scheme, palette]', function(newVals, oldVals) {
        setScale(newVals[0]);
        updateData(scope.data);
      });

      function setScale(scaleId) {
        switch(scaleId) {
          // Quantize
          case 0:
            if (scope.palette && scope.range) {
              scale = d3.scale.quantize()
                .domain([scope.domain.min, scope.domain.max])
                .range(d3.range(scope.range).map(function(i) {
                  return colorbrewer[scope.palette][scope.range][i];
                }));
            }
            break;

          // Non-Quantize
          case 1:
            if (scope.palette && scope.range) {
              var palette = colorbrewer[scope.palette][scope.range];

              var color1 = palette[0];
                color2 = palette[palette.length -1];

              scale = d3.scale.log()
                .domain([scope.domain.non_zero_min, scope.domain.non_zero_max])
                .range([color1, color2])
                .clamp(true);
            }
            break;

          // No scale
          default:
            scale = function() {
              return "none";
            };
        }
        return scale;
      }

      function updateData(data) {
        svg.select("#entities").selectAll("path")
          .attr('class', null)
          .attr('fill', function(d) {
            data.forEach(function(d) { rateById.set(d.cartogram_entity, d.value); });
            return fill(d);
          });
      }

      function fill(d) {
         value = rateById.get(d.properties.fips);
         if (value === null) {
           return 'none';
         } else {
           return scale(rateById.get(d.properties.fips));
         }
      }

      function ready(error, texas) {
        svg.append("g")
          .attr("id", "entities")
        .selectAll("path")
         .data(topojson.feature(texas, texas.objects.counties).features)
        .enter().append("path")
          .attr("id", function(d) { return d.properties.fips; })
          .attr("fill", function(d) { return fill(d); })
          .attr("d", path);

        if (hasLoader) {
            choropleth.find('#loader').fadeOut('slow', function() {
              this.remove();
              $('svg').fadeIn('slow');
            });
        }
      }

      function render(data) {
        data.forEach(function(d) {rateById.set(d.cartogram_entity, d.value); });
        queue()
          .defer(d3.json, "/static/JSON/texas.json")
          .await(ready);
      }

      render(scope.data);
    }
  };
});

// Live edit and generic rendering directive for Markdown
App.directive('markdown', function($window) {
  var converter = new $window.Showdown.converter();
  return {
    restrict: 'E',
    scope: {
      description: '='
    },
    link: function(scope, element, attrs) {
      function markdownify(html) {
        var htmlText = converter.makeHtml(html);
        element.html(htmlText);
      }

      // For static viewing
      if (!scope.description) {
        markdownify(element.text());
      }

      // For live editing
      scope.$watch('description', function(newVal, oldVal) {
        if (newVal) {
          markdownify(newVal);
        }
      });
    }
  };
});

App.controller('AbstractController', function AbstractController ($scope, $http, Palettes) {

  $scope.tab = 1;

  $scope._success = function() {
    window.location = "/choropleths/";
  };

  $scope.schemes = [
    {name: "Sequential", id: 1},
    {name: "Diverging", id: 2},
    {name: "Qualitivative", id: 3}
  ];

  // Update the number data_classes available based on the current palette selection
  $scope.$watch('palette', function (palette) {
    var keys, min, max;

    keys = [];
    if (palette) {
      for (var index in colorbrewer[palette.class_name]) keys.push(index);
      min = Math.min.apply(null, keys)
      max = Math.max.apply(null, keys)
    }
    $scope.range = {
      options: keys,
      min: min,
      max: max
    };
  });

  $scope.getSchemePalettes = function(id) {
    Palettes.query({id: id}, function(data) {
      $scope.palettes = data;
      $scope.findPalette($scope.choropleth.palette);
    });
  };

  $scope.findPalette = function(id) {
    if (0 < $scope.palettes.length) {

      // Set defaults if the choropleth doesn't already have values
      $scope.palette = $scope.palettes[0];
      $scope.choropleth.palette = $scope.palette.id;

      // Set palette if the palette id is in the palettes array
      $scope.palettes.forEach(function (value, index, array) {
        if (value.id == id) {
          $scope.palette = value;
          $scope.choropleth.palette = value.id;
        }
      });
    }
  };
});

App.controller('ViewController', function ViewController ($scope, $controller, Choropleth, Dataset, Palettes ) {
  $controller('AbstractController', {$scope: $scope});

  $scope.init = function(id) {
    Choropleth.get({id: id}, function (data) {
      $scope.choropleth = data;

      Dataset.get({id: data.dataset}, function(data) {
        $scope.dataset = data;
        $scope.scales = data.scale_options;
        $scope.hasData = true;
      });

      Palettes.query({id: data.scheme}, function (data) {
        $scope.palettes = data;
        $scope.findPalette($scope.choropleth.palette);
      });
    });
  };
});

App.controller('EditController', function EditController ($scope, $controller, Choropleth, Dataset, Palettes) {
  $controller('ViewController', {$scope: $scope});

  $scope.submit = function() {
    $('#saving-choropleth-modal').modal();
    $scope.choropleth.$update($scope._success);
  };

  $scope.delete = function() {
    $scope.choropleth.$delete($scope._success);
  };
});

App.controller('MappCtrl', function MappCtrl ($scope, $controller, Choropleth, Dataset, Palettes) {
  $controller('AbstractController', {$scope: $scope});

  $scope.init = function(id) {
    $scope.choropleth = new Choropleth();

    Dataset.get({id: id}, function(data) {
      $scope.dataset = data;
      $scope.choropleth.dataset = data.id;
      $scope.choropleth.name = data.name;
      $scope.choropleth.data_classes = 3;
      $scope.scales = data.scale_options;
      $scope.hasData = true;
    });

    Palettes.query({id: 1}, function(data) {
      $scope.palettes = data;
    });
  };

  $scope.submit = function() {
    $('#saving-choropleth-modal').modal();
    $scope.choropleth.$save($scope._success);
  };
});

