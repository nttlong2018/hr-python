(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('hcsDialog', dialog);

    dialog.$inject = ['templateService'];
    
    function dialog(templateService) {
        // Usage:
        //     <hcs-dialog></hcs-dialog>
        // Creates:
        // 
        var directive = {
            link: link,
            templateUrl: templateService.getTemplatePath('dialog'),
            restrict: 'EA'
        };
        return directive;

        function link(scope, element, attrs) {
        }
    }

})();