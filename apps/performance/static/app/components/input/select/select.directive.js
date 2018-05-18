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
            template: `
<div ng-controller="SelectpickerPanelCtrl as selectpickerVm" class="zb-form-select" >
    <ui-select ng-model="selectedItem.selected" class="btn-group bootstrap-select form-control" ng-disabled="false" append-to-body="true" search-enabled="true">
        <ui-select-match placeholder="{{placeholder}}">
            {{$select.selected.__fieldCaption}}
        </ui-select-match>
        <ui-select-choices repeat="searchItem in selectWithSearchItems | filter: $select.search">
            <span ng-bind-html="searchItem.__fieldCaption"></span>
        </ui-select-choices>
    </ui-select>
</div>
`,
            //templateUrl: "app/components/input/select/select.html",
            link: function ($scope, elem, attr) {
                var cmp = $(elem);
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