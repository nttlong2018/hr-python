(function () {
  'use strict';

  angular.module('ZebraApp.components.inputs')
      .directive('inputTextarea', inputTextarea);

  /** @ngInject */
    function inputTextarea() {
    return {
      restrict: 'E',
      replace: true,
      transclude: true,
      //template: function(el, attrs) {
      //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
      //}
      template: '<textarea class="form-control zb-form-textarea"></textarea>',
      //templateUrl: "app/components/input/text/text.html",
      link: function( $scope, elem, attr) {
          if(attr["required"]){
            $(elem).wrap("<span zb-required></span>")
          }
          //var input = $(elem.find("input")[0]);
      }
    };
  }
})();