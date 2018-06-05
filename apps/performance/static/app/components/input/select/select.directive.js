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
            templateUrl: "../performance/static/app/components/input/select/select.html",
            link: function ($scope, elem, attr) {
                var cmp = $(elem);
                if (attr["required"]) {
                    cmp.attr("zb-required", '');
                }
                //$compile(cmp.contents())($scope);
                var list = attr["list"];
                var ngModel = attr["ngModel"];
                var placeholder = attr["placeholder"];
                var fieldValue = attr["value"];
                var fieldCaption = attr["caption"];

                $scope.selectedItem = {};

                $scope.fieldValue = fieldValue;
                $scope.fieldCaption = fieldCaption;
                if (placeholder) {
                    $scope.placeholder = placeholder;
                }
                if (list) {
                    var dataList = $scope.$eval(list);
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
                        var retval = ((val && val[fieldValue]) || val[fieldValue] == false) ? val[fieldValue] : null;
                        $parse(ngModel).assign($scope.$parent, retval);
                    });
                }
            }
        };
    }

    angular.module('ZebraApp.components.inputs')
        .controller('SelectpickerPanelCtrl', SelectpickerPanelCtrl);

    function SelectpickerPanelCtrl($scope, $sce) { }

})();