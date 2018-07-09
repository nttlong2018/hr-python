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
            scope: {
                model: "=ngModel",
                caption: "@",
                fnChange: "=ngChange",
                disabled: "="
            },
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            templateUrl: "app/components/input/checkbox/checkbox.html",
            link: function ($scope, elem, attr) {
                var input = $(elem.find("input")[0]);
                var div = $(elem);

                if ($scope.disabled) {
                    input.prop("disabled", true);
                    div.addClass("disabled");
                } else {
                    input.prop("disabled", false);
                    div.removeClass("disabled");
                }
                $(elem).find("input[type=checkbox]").change(function () {
                    // if($(this).is(":checked")) {
                    //     var returnVal = confirm("Are you sure?");
                    //     $(this).attr("checked", returnVal);
                    // }
                    // $('#textbox1').val($(this).is(':checked')); 
                    if ($scope.fnChange) {
                        $scope.fnChange();
                    }
                });
            }
        };
    }
})();