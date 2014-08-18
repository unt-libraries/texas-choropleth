var d3MappApp = angular.module('d3MappApp', []);

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

            // Draw the initial SVG
            var svg = d3.select(element[0]).append("svg")
                .attr("width", width)
                .attr("height", height);

            // Legend SVGs
            var legend = svg.selectAll('g.legendEntry')
                .data(quantize.range())
                .enter()
                .append('g').attr('class', 'legendEntry')


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
                  .attr("class", function(d) { return quantize(rateById.get(d.properties.countyCode)); });
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

d3MappApp.directive('markdown', function($window) {
    var converter = new $window.Showdown.converter();
    return {
        restrict: 'E',
        scope: {
            description: '='
        },
        link: function(scope, element, attrs) {
            scope.$watch('description', function(description) { 
                var htmlText = converter.makeHtml(description);
                element.html(htmlText)
            })
        }
    }
});

d3MappApp.controller('AbstractController', function AbstractController ($scope, $http) {

    $scope.domain = {min: 0, max: .15};
        $scope.rangeOptions = [3, 4, 5, 6, 7, 8, 9];
        $scope.schemes = [
            {name: "Sequential", id: 1},
            {name: "Diverging", id: 2},
            {name: "Qualitivative", id: 3}
        ];

    $scope.getSchemePalettes = function(id) {
        var palettes = "/choropleths/api/palettes/" + id + "/";
        $http.get(palettes).success(function(data, status, headers, config) {
            $scope.palettes = data
            $scope.findPalette($scope.choropleth.palette)
        })
    }

    $scope.findPalette = function(id) {
        if (0 < $scope.palettes.length) {
            $scope.palettes.forEach(function (value, index, array) {
                if (value.id == id) {
                    $scope.palette = value;
                }
            });
        }
    }

})

d3MappApp.controller('ViewController', function ViewController ($scope, $http, $controller) {
    $controller('AbstractController', {$scope: $scope});
    var choroplethBaseUrl = "/choropleths/api/"; 
    var datasetsBaseUrl = "/datasets/api/";

    $scope.init = function(id) {
        var url = choroplethBaseUrl + "" + id + "/";
        $http.get(url).success(function(data, status, headers, config) {
            $scope.choropleth = data;
            
            // Set the saved palette
            $scope.palette = {}
            $scope.palette.class_name = data.palette

            datasetID = data.dataset;

            var url = datasetsBaseUrl + datasetID + "/";
            $http.get(url).success(function(data, status, headers, config) {
                $scope.dataset = data;
                $scope.hasData = true;
                $scope.getSchemePalettes($scope.choropleth.scheme)
            }).
            error(function(data, status, headers, config) {
                console.log(data);
            });
        }).
        error(function(data, status, headers, config) {
            console.log(data);
        });

    };

});

d3MappApp.controller('EditController', function EditController ($scope, $http, $controller) {
    $controller('ViewController', {$scope: $scope});
    var choroplethBaseUrl = "/choropleths/api/"; 
    var datasetsBaseUrl = "/datasets/api/";

    $scope.submit = function() {
        console.log($scope.choropleth)
        var url = choroplethBaseUrl + $scope.choropleth.id + "/";
        $http.put(url, $scope.choropleth).success(function(data, status) {
            if (status == 200) {
                window.location = "/choropleths/";
            }
        });
    }

    $scope.delete = function() {
        console.log($scope.choropleth)
        var url = choroplethBaseUrl + $scope.choropleth.id + "/";
        if (confirm("Are you sure you want to delete this choropleth?")) {
            $http.delete(url).success(function(data, status) {
                console.log(status)
                if (status == 204) {
                    window.location = "/choropleths/";
                }
            });
        }
    }

});

d3MappApp.controller('MappCtrl', function MappCtrl ($scope, $http, $controller) {
    $controller('AbstractController', {$scope: $scope});
    var datasetsBaseUrl = "/datasets/api/";
    $scope.hasData = false;

    $scope.init = function(id) {
        var choropleth = {
            name: "",
            description: "",
            published: 0,
            scheme: 1,
            palette: 1,
            data_classes: 9,
            dataset: id,
            owner: 1
        }

        var url = datasetsBaseUrl + id + "/";

        $http.get(url).success(function(data, status, headers, config) {
            $scope.choropleth = choropleth
            $scope.dataset = data
            $scope.hasData = true;
            var palettes = "/choropleths/api/palettes/" + choropleth.scheme + "/";
            $http.get(palettes).success(function(data, status, headers, config) {
                $scope.palettes = data
            })
        }).
        error(function(data, status, headers, config) {
            console.log(data);
        });
    };

    $scope.submit = function() {
        $http.post("/choropleths/api/", $scope.choropleth).success(function(data, status) {
            if (status == 201) {
                window.location = "/choropleths/";
            }
        });
    };
});

