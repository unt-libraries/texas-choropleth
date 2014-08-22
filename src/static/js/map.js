var d3MappApp = angular.module('d3MappApp', ['ngResource']);

d3MappApp.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
})

d3MappApp.directive('choropleth', function($window) {

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
            scale: '=',
            scheme: '=',
        },
        link: function (scope, element, attrs) {

            // Scaling function
            var quantize = d3.scale.quantize()
                .domain([scope.domain.min, scope.domain.max])
                .range(d3.range(scope.range).map(function(i) { return "q" + i + "-" + scope.range; }));

            var tip = d3.tip()
                .attr('class', 'd3-tip')
                .html(function(d, i) {
                    return "<span><strong>FIPS</strong>: " + d.properties.countyCode + "</span><br>"
                    + "<span><strong>Name</strong>: "+ d.properties.countyName + "</span><br> "
                    + "<span><strong>Value</strong>: " + rateById.get(d.properties.countyCode) + "</span>"
                });

            // Draw the initial SVG
            var svg = d3.select(element[0]).append("svg")
                .attr("width", width)
                .attr("height", height)
                .call(tip);

            // Legend SVGs
            var legend = svg.selectAll('g.legendEntry')
                .data(quantize.range())
                .enter()
                .append('g').attr('class', 'legendEntry');


            function updateData(data) {
                svg.select("#counties").selectAll("path")
                    .attr('class', null)
                    .attr('class', function(d) {
                        data.forEach(function(d) { rateById.set(d.cartogram_entity, +d.value); })
                        return quantize(rateById.get(d.properties.countyCode));
                    })
            }

            function updateDomainAndRange(newDomain) {
                quantize = d3.scale.quantize()
                    .domain([scope.domain.min, scope.domain.max])
                    .range(d3.range(scope.range).map(function(i) { return "q" + i + "-" + scope.range; }));

                updateData(scope.data);
                drawLegend();
            }

            function drawLegend() {
                svg.selectAll('g.legendEntry').remove();
                var legend = svg.selectAll('g.legendEntry')
                    .data(quantize.range())
                    .enter()
                    .append('g').attr('class', 'legendEntry')

                legend.append('rect')
                    .attr("x", width - 580)
                    .attr("y", function(d, i) {return (i * 10) + 50;})
                    .attr("width", 10)
                    .attr('height', 10)
                    .attr("class", function(d) {return d })

                legend.append('text')
                    .attr("x", width - 565)
                    .attr("y", function(d, i) {return  (i*10) + 50} )
                    .attr('dy', "1em")
                    .style("font-size", "10px")
                    .text(function(d,i) {
                        var extent = quantize.invertExtent(d);
                        var format = d3.format("0.2f")
                        return format(+extent[0])+ " - " + format(+extent[1]);
                    })
            }

            function ready(error, texas) {
              svg.append("g")
                  .attr("id", "counties")
                .selectAll("path")
                 .data(topojson.feature(texas, texas.objects.counties).features)
                .enter().append("path")
                  .attr("id", function(d) { return d.properties.countyCode })
                  .attr("d", path)
                  .attr("class", function(d) {return quantize(rateById.get(d.properties.countyCode)); })
                  .on('mouseover', tip.show)
                  .on('mouseout', tip.hide);
            }

            function render(data) {
                data.forEach(function(d) {rateById.set(d.cartogram_entity, +d.value); });
                queue()
                    .defer(d3.json, "/static/JSON/texas.json")
                    .await(ready);
            }

            render(scope.data);

            /* ---- Watchers ---- */

            // Watch for changes in the dataset
            scope.$watch('data', function(newVals, oldVals) {
                updateData(newVals);
            }, true);

            // Watch for changes in the domain inputs
            scope.$watch('domain', function(newVals, oldVals) {
                updateDomainAndRange(newVals);
            }, true);

            // Watch for changes in the range
            scope.$watch('range', function(newVals, oldVals) {
                updateDomainAndRange(newVals);
            }, true);

        }
    }
});

d3MappApp.factory('Choropleth', function($resource) {
    return $resource('/choropleths/api/:id/ ', { id: '@id' }, {
        update: {
            method: 'PUT'
        }
    });
});

d3MappApp.factory('Dataset', function($resource) {
    return $resource('/datasets/api/:id/ ');
});

d3MappApp.factory('Palettes', function($resource) {
    return $resource('/choropleths/api/palettes/:id/ ');
});

d3MappApp.directive('markdown', function($window) {
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
            })
        }
    }
});

d3MappApp.controller('AbstractController', function AbstractController ($scope, $http, Palettes) {

    $scope.tab = 1;

    $scope._success = function() {
        window.location = "/choropleths/";
    }

    $scope.domain = {min: 0, max: .15};
        $scope.rangeOptions = [3, 4, 5, 6, 7, 8, 9];
        $scope.schemes = [
            {name: "Sequential", id: 1},
            {name: "Diverging", id: 2},
            {name: "Qualitivative", id: 3}
        ];

    $scope.getSchemePalettes = function(id) {
        Palettes.query({id: id}, function(data) {
            $scope.palettes = data;
            $scope.findPalette($scope.choropleth.palette);
        })
    };

    $scope.findPalette = function(id) {
        if (0 < $scope.palettes.length) {
            $scope.palettes.forEach(function (value, index, array) {
                if (value.id == id) {
                    $scope.palette = value;
                };
            });
        };
    };
});

d3MappApp.controller('ViewController', function ViewController ($scope, $controller, Choropleth, Dataset, Palettes ) {
    $controller('AbstractController', {$scope: $scope});

    $scope.init = function(id) {
        Choropleth.get({id: id}, function (data) {
            $scope.choropleth = data;
            
            Dataset.get({id: data.dataset}, function(data) {
                $scope.dataset = data;
                $scope.hasData = true;
            });

            Palettes.query({id: data.scheme}, function (data) {
                $scope.palettes = data;
                $scope.findPalette($scope.choropleth.palette);
            });
        });
    };
});

d3MappApp.controller('EditController', function EditController ($scope, $controller, Choropleth, Dataset, Palettes) {
    $controller('ViewController', {$scope: $scope});

    $scope.submit = function() {
        $scope.choropleth.$update($scope._success);
    };

    $scope.delete = function() {
        if (confirm("Are you sure you want to delete this choropleth?")) {
            $scope.choropleth.$delete($scope._success);
        };
    };

});

d3MappApp.controller('MappCtrl', function MappCtrl ($scope, $controller, Choropleth, Dataset, Palettes) {
    $controller('AbstractController', {$scope: $scope});
    var datasetsBaseUrl = "/datasets/api/";
    $scope.hasData = false;

    $scope.init = function(id) {
        $scope.choropleth = new Choropleth()

        Dataset.get({id: id}, function(data) {
            $scope.dataset = data;
            $scope.choropleth.dataset = data.id;
            $scope.choropleth.name = data.name;
            $scope.hasData = true;
        });

        Palettes.query({id: 1}, function(data) {
            $scope.palettes = data;
        });
    };

    $scope.submit = function() {
        $scope.choropleth.$save($scope._success);
    };
});

