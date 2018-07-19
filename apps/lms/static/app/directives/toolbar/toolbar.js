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
                onSearch: '&',
                onAdd: '&',
                onCopy: '&',
                onDelete: '&',
                onEdit: '&',
                onSave: '&',
                onUndo: '&',
                onPrint: '&',
                onSetting: '&',
                onExport: '&',
                onImport: '&',
            },
            templateUrl: templateService.getTemplatePath('toolbar'),
            restrict: 'EA'
        };
        return directive;

        function link(scope, element, attrs) {
            element.find('#hcs-admin-system-txtSearch').bind('keyup', function (e) {
                if (e.keyCode === 13) { // 13 is enter key
                    // Execute code here.
                    scope.onSearch();
                }
            });

        }
    }

})();