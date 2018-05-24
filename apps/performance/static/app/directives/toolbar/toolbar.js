(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('hcsToolBar', toolbar);

    toolbar.$inject = ['templateService'];
    
    function toolbar(templateService) {
        // Usage:
        //     <hcs-tool-bar></hcs-tool-bar>
        // Creates:
        // 
        var directive = {
            link: link,
            scope: {
                searchCommon: '=searchCommon',
                onAdd: '&',
                onCopy: '&',
                onDelete: '&',
                onEdit: '&',
                onSave: '&',
                onUndo: '&',
                onPrint: '&',
                onSetting: '&'
            },
            templateUrl: templateService.getTemplatePath('toolbar'),
            restrict: 'EA'
        };
        return directive;

        function link(scope, element, attrs) {
        }
    }

})();