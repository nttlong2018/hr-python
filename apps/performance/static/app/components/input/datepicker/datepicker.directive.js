(function () {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('datePicker', ["$parse", "$filter", "$sce", inputSelect]);

    /** @ngInject */
    function inputSelect($parse, $filter, $sce) {
        return {
            restrict: 'E',
            replace: true,
            scope: {
                dt: "=ngModel",
                format: "@"
            },
            //transclude: true,
            //template: '<input type="text" class="form-control zb-form-input"/>',
            templateUrl: "app/components/input/datepicker/datepicker.html",
            link: function ($scope, elem, attr) {
                if (attr["required"]) {
                    $(elem).attr("zb-required", '');
                }

                $scope.opened = false;
                $scope.format = ($scope.format) ? $scope.format : 'dd-MM-yyyy';
                $scope.options = {
                    showWeeks: false
                };

                $loadLayout($scope, elem, attr);

                $scope.$watch("dt", function (val, old) {
                    $scope.opened = false;
                    // if (val) {
                    //     $scope.dt = new Date($scope.dt);
                    // } else {    
                    //     $scope.dt = new Date();
                    // }
                    if (!angular.isDate(val)) {
                        $scope.dt = ($scope.dt) ? new Date($scope.dt) : new Date();
                    }

                    $scope.$applyAsync();
                });
            }
        };
    }

    function $loadLayout($scope, elem, attr) {
        var btnCalendar = $(elem.find("button.btn-default")[0]);
        var inputDate = $(elem.find("input")[0]);

        function calendar_in() {
            inputDate.addClass("zb-form-date-picker-focus");
            btnCalendar.addClass("zb-form-date-picker-focus");
        }

        function calendar_out() {
            inputDate.removeClass("zb-form-date-picker-focus");
            btnCalendar.removeClass("zb-form-date-picker-focus");
        }

        btnCalendar.unbind("click");
        btnCalendar.bind("click", function () {
            $scope.opened = true;
            $scope.$apply();
        });

        btnCalendar.unbind("mouseenter");
        btnCalendar.bind("mouseenter", function () {
            calendar_in();
        });

        btnCalendar.unbind("mouseleave");
        btnCalendar.bind("mouseleave", function () {
            calendar_out();
        });

        inputDate.unbind("focusin");
        inputDate.bind("focusin", function () {
            if ($scope.opened) {
                $scope.opened = false;
                $scope.$applyAsync();
                calendar_in
                btnCalendar.focus();
            } else {
                calendar_in();
                $scope.opened = true;
                $scope.$applyAsync();
            }
        });

        inputDate.unbind("focusout");
        inputDate.bind("focusout", function () {
            calendar_out();
        });
    }

    //angular.module('ZebraApp.components.inputs')
    //    .controller('datepickerpopupCtrl', datepickerpopupCtrl)
    //    .controller('datepickerCtrl', datepickerCtrl);

    /** @ngInject */
    /*function datepickerpopupCtrl($scope) {
        $scope.open = open;
        $scope.opened = false;
        $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
        $scope.format = $scope.formats[0];
        $scope.options = {
            showWeeks: false
        };

        function open() {
            $scope.opened = true;
        }
    }*/

    /** @ngInject */
    /*function datepickerCtrl($scope) {

        $scope.dt = new Date();
        $scope.options = {
            showWeeks: false
        };

    }*/

})();