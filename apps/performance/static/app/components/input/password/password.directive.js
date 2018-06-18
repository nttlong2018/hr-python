(function() {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('inputPassword', password);

    password.$inject = ['$window'];
    
    function password ($window) {
        // Usage:
        //     <input-password></input-password>
        // Creates:
        // 
        var directive = {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                result: "="
            },
            template: '<input type="password" class="form-control zb-form-input"/>',
            link: link
        };
        return directive;

        function link(scope, element, attrs) {
            if (attrs["required"]) {
                $(element).wrap("<span zb-required></span>")
            }
        }

        
    }

})();