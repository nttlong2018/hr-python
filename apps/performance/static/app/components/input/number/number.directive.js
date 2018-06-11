(function () {
  'use strict';

  angular.module('ZebraApp.components.inputs')
      .directive('inputNumber', inputText);

  /** @ngInject */
  function inputText() {
    return {
      restrict: 'E',
      replace: true,
      transclude: true,
      //template: function(el, attrs) {
      //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
      //}
        template: '<input type="number" class="form-control zb-form-input" value="0" min="0" />',
      //templateUrl: "app/components/input/text/text.html",
        link: function ($scope, elem, attr) {
            if (attr["required"]) {
                $(elem).wrap("<span zb-required></span>")
            }
          //var input = $(elem.find("input")[0]);
          //var placeholder = attr["placeholder"];
      }
    };
  }
})();