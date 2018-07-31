'use strict';

(function () {

    var ServiceNowXLQueryTileViewController = function ($scope, ServiceNowXLQueryService, XlrTileHelper) {
        var vm = this;
        var tile;
        var config;
        var predefinedColors = [];
        predefinedColors['New'] = '#7E827A';
        predefinedColors['Active'] = '#4AA0C8';
        predefinedColors['Open'] = '#FFA500';
        predefinedColors['Awaiting Problem'] = '#7E8AA2';
        predefinedColors['Awaiting User Info'] = '#7FB2F0';
        predefinedColors['Awaiting Evidence'] = '#45BF55';
        predefinedColors['Resolved'] = '#FFE11A';
        predefinedColors['Closed'] = '#FFA500';


        var colorPool = [
            '#B85C5A',
            '#35203B',
            '#644D52',
            '#8E2800',
            '#FF8598',
            '#FF6F69',
            '#F77A52',
            '#FCD364',
            '#FFE11A'
        ];


        if ($scope.xlrTile) {
            // summary mode
            tile = $scope.xlrTile.tile;
        } else {
            // details mode
            tile = $scope.xlrTileDetailsCtrl.tile;
        }

        function tileConfigurationIsPopulated() {
            // old style pre 7.0
            if (tile.properties == null) {
                config = tile.configurationProperties;
            } else {
                // new style since 7.0
                config = tile.properties;
            }
            return !_.isEmpty(config.servicenowServer);
        }

        function getColor(value) {
            if (predefinedColors[value]) return predefinedColors[value];
            return colorPool.pop();
        }

        function getTitle(){
            if(vm.issuesSummaryData.total > 1){
                return "tickets";
            }
            else{
                return "ticket";
            }
        }

        vm.chartOptions = {
            topTitleText: function (data) {
                return data.total;
            },
            bottomTitleText: getTitle,
            series: function (data) {
                var series = {
                    name: 'State',
                    data: []
                };
                series.data = _.map(data.data, function (value) {
                    return {y: value.counter, name: value.state, color: value.color};
                });
                return [ series ];
            },
            showLegend: false,
            donutThickness: '60%'
        };

        function load(config) {
            if (tileConfigurationIsPopulated()) {
                vm.loading = true;
                ServiceNowXLQueryService.executeQuery(tile.id, config).then(
                    function (response) {
                        var serviceNowIssueArray = [];
                        var issues = response.data.data;
                        if(issues[0] === "Invalid table name"){
                            vm.invalidTableName = true;
                        }
                        else{
                            vm.invalidTableName = false;
                            vm.states = [];
                            vm.statesCounter = 0;
                            vm.issuesSummaryData = {
                                data: null,
                                total: 0
                            };
                            vm.issuesSummaryData.data = _.reduce(issues, function (result, value) {
                                var state = value.state;
                                vm.issuesSummaryData.total += 1;
                                if (result[state]) {
                                result[state].counter += 1;
                            } else {
                                result[state] = {
                                    counter: 1,
                                    color: getColor(state),
                                    state: state
                                };
                            }
                            value.color = result[state].color;
                            serviceNowIssueArray.push(value);
                            return result;

                        }, {});
                        _.forEach(vm.issuesSummaryData.data, function (value, key) {
                            if (vm.statesCounter < 5) vm.states.push(value);
                            vm.statesCounter++;
                        });
                        vm.gridOptions = createGridOptions(serviceNowIssueArray);
                        }
                    }
                ).finally(function () {
                    vm.loading = false;

                });
            }
        }

        function createGridOptions(serviceNowData) {
            var filterHeaderTemplate = `<div data-ng-include="partials/releases/grid/templates/name-filter-template.html"></div>`;
            var columnDefs = [
                    {
                        displayName: "Number",
                        field: "number",
                        cellTemplate: "static/@project.version@/include/ServiceNowXLQueryTile/grid/number-cell-template.html",
                        filterHeaderTemplate: filterHeaderTemplate,
                        enableColumnMenu: true,
                        width: '18%'
                    }
                ];
            for (var key in config.detailsViewColumns['value']) {
                if (key != "number") {
                    columnDefs.push({displayName: key, field: key, filterHeaderTemplate: filterHeaderTemplate, enableColumnMenu: true})
                }
            };
            return XlrTileHelper.getGridOptions(serviceNowData, columnDefs);
        }

        function refresh() {
            load({params: {refresh: true}});
        }

        load();

        vm.refresh = refresh;
    };

    ServiceNowXLQueryTileViewController.$inject = ['$scope', 'xlrelease.serviceNowXL.ServiceNowXLQueryService', 'XlrTileHelper'];

    var ServiceNowXLQueryService = function (Backend) {

        function executeQuery(tileId, config) {
            return Backend.get("/tiles/" + tileId + "/data", config);
        }
        return {
            executeQuery: executeQuery
        };
    };

    ServiceNowXLQueryService.$inject = ['Backend'];

    angular.module('xlrelease.ServiceNowXL.tile', []);
    angular.module('xlrelease.ServiceNowXL.tile').service('xlrelease.serviceNowXL.ServiceNowXLQueryService', ServiceNowXLQueryService);
    angular.module('xlrelease.ServiceNowXL.tile').controller('serviceNowXL.ServiceNowXLQueryTileViewController', ServiceNowXLQueryTileViewController);

})();

