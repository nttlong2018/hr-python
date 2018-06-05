(function() {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('datePicker', ["$parse", "$filter", "$sce", inputSelect]);

    /** @ngInject */
    function inputSelect($parse, $filter, $sce) {
        return {
            restrict: 'E',
            replace: true,
            scope: true,
            //transclude: true,
            template: `
<p class="input-group zb-form-date-picker">
    <input type="text" class="form-control" uib-datepicker-popup="{{format}}" datepicker-options="options" ng-model="dt" is-open="opened" ng-required="false" close-text="Close" alt-input-formats="altInputFormats" show-button-bar="true" type="date" placeholder="{{placeholder}}" />
    <span class="input-group-btn">
      <button type="button" class="btn btn-default"><i class="glyphicon glyphicon-calendar"></i></button>
    </span>
</p>
`,
            //templateUrl: "app/components/input/datepicker/datepicker.html",
            link: function($scope, elem, attr) {
                var ngModel = attr["ngModel"];
                var format = attr["format"];

                if (attr["required"]) {
                    $(elem).attr("zb-required", '');
                }

                $scope.opened = false;
                $scope.format = (format) ? format : 'dd-MM-yyyy';
                $scope.options = {
                    showWeeks: false
                };
                var $dt = null;
                if (ngModel && $scope.$eval(ngModel)) {
                    $dt = new Date($scope.$eval(ngModel));
                } else {
                    $dt = new Date();
                }
                $scope.dt = $dt;
                $scope.setDate = function(year, month, day) {
                    $scope.dt = new Date(year, month, day);
                };

                $loadLayout($scope, elem, attr);

                $scope.$watch("dt", function(val, old) {
                    $scope.opened = false;
                    $scope.$applyAsync();
                    $parse(ngModel).assign($scope, val);
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
        btnCalendar.bind("click", function() {
            $scope.opened = true;
            $scope.$apply();
        });

        btnCalendar.unbind("mouseenter");
        btnCalendar.bind("mouseenter", function() {
            calendar_in();
        });

        btnCalendar.unbind("mouseleave");
        btnCalendar.bind("mouseleave", function() {
            calendar_out();
        });

        inputDate.unbind("focusin");
        inputDate.bind("focusin", function() {
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
        inputDate.bind("focusout", function() {
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