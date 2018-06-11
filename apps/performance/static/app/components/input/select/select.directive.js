(function () {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('inputSelect', ["$parse", "$filter", "$sce", inputSelect]);

    /** @ngInject */
    function inputSelect($parse, $filter, $sce) {
        return {
            restrict: 'E',
            replace: true,
            scope: true,
            //transclude: true,
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            templateUrl: "app/components/input/select/select.html",
            link: function ($scope, elem, attr) {
                var cmp = $(elem);
                //$compile(cmp.contents())($scope);
                var list = attr["list"];
                var ngModel = attr["ngModel"];
                var placeholder = attr["placeholder"];
                var fieldValue = attr["value"];
                var fieldCaption = attr["caption"];

                function compile() {
                    if (attr["required"]) {
                        cmp.attr("zb-required", '');
                    }

                    $scope.selectedItem = {};

                    $scope.fieldValue = fieldValue;
                    $scope.fieldCaption = fieldCaption;
                    if (placeholder) {
                        $scope.placeholder = placeholder;
                    }
                    if (list) {
                        var dataList = $scope.$parent.$eval(list);
                        console.log($scope, dataList)
                        $.each(dataList, function (i, v) {
                            v["__fieldCaption"] = $sce.trustAsHtml(v[fieldCaption]);
                        });
                        $scope.selectWithSearchItems = dataList;
                        var ngModelVal = $scope.$eval(ngModel);
                        if (ngModelVal) {
                            var $selectedItem = $filter('filter')($scope.selectWithSearchItems, function (f) {
                                return f[fieldValue] == ngModelVal;
                            });
                            if ($selectedItem.length > 0) {
                                $scope.selectedItem = {
                                    selected: $selectedItem[0]
                                };
                            }
                        }
                        $scope.$watch("selectedItem.selected", function (val, old) {
                            var retval = (val && val[fieldValue]) ? val[fieldValue] : null;
                            $parse(ngModel).assign($scope.$parent, retval);
                        });
                    }
                }

                $scope.$parent.$watch(list, function (val, old) {
                    compile();
                });
            }
        };
    }

    angular.module('ZebraApp.components.inputs')
        .controller('SelectpickerPanelCtrl', SelectpickerPanelCtrl);

    function SelectpickerPanelCtrl($scope, $sce) { }

})();