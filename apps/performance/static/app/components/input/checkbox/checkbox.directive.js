(function () {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('inputCheckbox', ["$parse", inputCheckbox]);

    /** @ngInject */
    function inputCheckbox($parse) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: true,
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            templateUrl: "../performance/static/app/components/input/checkbox/checkbox.html",
            link: function ($scope, elem, attr) {
                var input = $(elem.find("input")[0]);
                var div = $(elem);
                var ngModel = attr["ngModel"];
                var caption = attr["caption"];
                var ngChange = attr["ngChange"];
                var disabled = attr["disabled"];

                if (ngModel) {
                    $scope.model = ($scope.$eval(ngModel)) ? $scope.$eval(ngModel) : null;
                }
                if (caption) {
                    $scope.caption = caption;
                }
                if (disabled == "true") {
                    input.prop("disabled", true);
                    div.addClass("disabled");
                } else {
                    input.prop("disabled", false);
                    div.removeClass("disabled");

                    $scope.$watch("model", function (val, old) {
                        $parse(ngModel).assign($scope.$parent, val);
                        if (ngChange) {
                            $scope.$eval(ngChange);
                        }
                    });
                }
            }
        };
    }
})();