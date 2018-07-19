(function () {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('inputSelect', ["$parse", "$filter", "$sce", inputSelect])
        .controller('SelectpickerPanelCtrl', SelectpickerPanelCtrl);

    /** @ngInject */
    function inputSelect($parse, $filter, $sce) {
        return {
            restrict: 'E',
            //replace: true,
            scope: {
                list: "=",
                ngModel: "=",
                placeholder: "@",
                fieldValue: "@value",
                fieldCaption: "@caption"
            },
            //transclude: true,
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            //template: '<input type="text" class="form-control zb-form-input"/>',
            templateUrl: "app/components/input/select/select.html",
            //controller: function($scope, $element, $attrs) {
            //    $scope.math = Math.random();
            //    console.log("++++++++++++++++++++++++++++++++++++++++++++");
            //    console.log($scope, $element, $attrs)
            //    console.log("++++++++++++++++++++++++++++++++++++++++++++");
            //},
            link: function ($scope, elem, attr) {
                var cmp = $(elem);
                //$compile(cmp.contents())($scope);
                if (attr["required"]) {
                    cmp.attr("zb-required", '');
                }
                $scope.selectedItem = {};
                $scope.$watch("list", function (val, old) {
                    if ($scope.list) {
                        $.each($scope.list, function (i, v) {
                            v["__fieldCaption"] = $sce.trustAsHtml(v[$scope.fieldCaption]);
                        });
                        $scope.selectWithSearchItems = $scope.list;
                        /*Watch model*/
                        var existsWatchModel = false;
                        if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                            existsWatchModel = _.filter($scope.$$watchers, function (f) {
                                return f.exp === "ngModel"
                            }).length > 0;
                        }
                        if (!existsWatchModel) {
                            $scope.$watch("ngModel", function (v) {
                                if ($scope.ngModel) {
                                    var $selectedItem = $filter('filter')($scope.selectWithSearchItems, function (f) {
                                        return f[$scope.fieldValue] == $scope.ngModel;
                                    });
                                    if ($selectedItem.length > 0) {
                                        $scope.selectedItem = {
                                            selected: $selectedItem[0]
                                        };
                                    }
                                }
                            });
                        }
                        /*Watch Selected Item*/
                        var existsWatch = false;
                        if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                            existsWatch = _.filter($scope.$$watchers, function (f) {
                                return f.exp === "selectedItem.selected"
                            }).length > 0;
                        }
                        if (!existsWatch) {
                            $scope.$watch("selectedItem.selected", function (val, old) {
                                var retval = (val && val[$scope.fieldValue]) ? val[$scope.fieldValue] : null;
                                $scope.ngModel = retval;
                            });
                        }
                    }
                });
            }
        };
    }
    function SelectpickerPanelCtrl($scope, $sce) { }
})();