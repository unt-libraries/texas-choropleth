App.directive('choropleth', function($http) {

  // Clone the loader
  var loader = $("#loader").clone();
  var hasLoader = loader.length > 0;

  // If loader is not present, do not hide the choropleth
  if (hasLoader) {
      var choropleth = $("#choropleth");
          choropleth.append(loader.show());
  }

  // Width and height of the SVG
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
    scope: true,
    link: function (scope, element, attrs) {
      var scale, svg, $svg, g;

      // D3 SVG Element added to the DOM
      svg = d3.select(element[0]).append("svg")
        .attr("width", width)
        .attr("height", height);

      // JQuery Object for manipulating the SVG's behavior
      $svg = $('svg');

      // Hide the loader only if the loader object exists
      hasLoader ? $svg.hide() : false;

      // Watch for change in the Entity selection
      scope.$watch('choropleth.selection.cartogram_entity', function(newVals, oldVals) {
          if (newVals !== oldVals) {
              var records = scope.dataset.records;
              records.forEach(function(record) {
                  if (newVals === record.cartogram_entity) {
                      scope.choropleth.selection = JSON.parse(JSON.stringify(record));
                  }
              });
          }
      });

      // Watch for changes in the Choropleth members items and in the selected Palette
      scope.$watchCollection('[choropleth.scale, choropleth.data_classes, palette.class_name]', function(newVals, oldVals) {
        setScale(newVals[0]);
        update(scope.dataset.records);
      });

      function legend(color1, color2) {
        var w =10, h = 400;

        d3.select('g#legend').remove();

        var key = d3.select("svg")
            .append("g")
            .attr('id', 'legend')
            .attr("width", w)
            .attr("height", h);

        var legend = key.append("defs")
            .append("svg:linearGradient")
            .attr("id", "gradient")
            .attr("x1", "100%")
            .attr("y1", "0%")
            .attr("x2", "100%")
            .attr("y2", "100%")
            .attr("spreadMethod", "pad");

        legend.append("stop")
          .attr("offset", "0%")
          .attr("stop-color", color2)
          .attr("stop-opacity", 1);

        legend.append("stop")
        .attr("offset", "100%")
          .attr("stop-color", color1)
          .attr("stop-opacity", 1);

        key.append("rect")
          .attr("width", w) 
          .attr("height", h - 100)
          .style("fill", "url(#gradient)")
          .attr("transform", "translate(25,10)");

        var y = d3.scale.linear()
          .range([300, 0])
          .domain([1, 100]);

        var yAxis = d3.svg.axis()
          .scale(y)
          .orient("right");

        key.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate(41,10)")
          .call(yAxis)
          .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 30)
          .attr("dy", ".80em")
          .style("text-anchor", "end")
          .text(scope.dataset.label);

      }

      // Determines correct scale for the current ScaleID
      function setScale(scaleId) {
        var range = scope.choropleth.data_classes;

        switch(scaleId) {
          // Quantize
          case 0:
            if (scope.palette && scope.choropleth.data_classes) {
              var min = scope.dataset.domain.min,
                  max = scope.dataset.domain.max;

              scale = d3.scale.quantize()
                .domain([min, max])
                .range(d3.range(range).map(function(i) {
                  return colorbrewer[scope.palette.class_name][range][i];
                }));
            }
            break;

          // Non-Quantize
          case 1:
            if (scope.palette && range) {
              var palette = colorbrewer[scope.palette.class_name][range];

              var color1 = palette[0];
                  color2 = palette[palette.length -1];

              var min = scope.dataset.domain.non_zero_min,
                  max = scope.dataset.domain.non_zero_max;

              scale = d3.scale.log()
                .domain([min, max])
                .range([color1, color2])
                .clamp(true);

              legend(color1, color2)
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

      //Updates the SVG/Path elements accordingly
      function update(data) {
        svg.select("#entities").selectAll("path")
          .attr('fill', function(d) {
            return fill(d);
          });
      }

      // Helper function to determine the fill color base on the dataset record value
      function fill(d) {
         value = rateById.get(d.properties.fips);
         if (value === null) {
           return 'none';
         }
         return scale(rateById.get(d.properties.fips));
      }

      // Performs the initial drawing operation for the Choropleth
      function ready(texas) {
        svg.append("g")
          .attr("id", "entities")
        .selectAll("path")
         .data(topojson.feature(texas, texas.objects.counties).features)
        .enter().append("path")
          .attr("id", function(d) { return d.properties.fips; })
          .attr("fill", function(d) { return fill(d); })
          .style('cursor', 'pointer')
          .on("mouseenter", function(d) {
            scope.choropleth.selection.cartogram_entity = d.properties.fips;
            scope.$apply();
          })
          .on("mouseleave", function(d) {
            scope.choropleth.selection = {};
            scope.$apply();
          })
          .attr("d", path);

        // Show the loader if it exists
        if (hasLoader) {
            choropleth.find('#loader').fadeOut('slow', function() {
              this.remove();
              $('svg').fadeIn('slow');
            });
        }
      }

      // Wrapper function for ready()
      // Grabs the TopoJson file and draws the Choropleth if the
      // call is successful
      function render(data) {
        data.forEach(function(d) {rateById.set(d.cartogram_entity, d.value); });
        $http.get('/static/JSON/texas.json')
        .success(function(data, status) {
            ready(data);
        });
      }

      // Begin execution
      render(scope.dataset.records);
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

App.controller('AbstractController', function AbstractController ($scope, $window, $http, Palettes) {

  $scope.tab = 1;

  $scope._success = function() {
    $window.location = "/choropleths/";
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
      min = Math.min.apply(null, keys);
      max = Math.max.apply(null, keys);
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
      $scope.choropleth.selection = {};

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
    $('#in-progress').modal();
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
      $scope.choropleth.selection = {};
      $scope.scales = data.scale_options;
      $scope.hasData = true;
    });

    Palettes.query({id: 1}, function(data) {
      $scope.palettes = data;
    });
  };

  $scope.submit = function() {
    $('#in-progress').modal();
    $scope.choropleth.$save($scope._success);
  };
});

