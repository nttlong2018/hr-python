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
                searchCommon: '=',
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

            scope.enableFunction = {
                Search : attrs['onSearch'],
                Add : attrs['onAdd'],
                Copy : attrs['onCopy'],
                Delete : attrs['onDelete'],
                Edit : attrs['onEdit'],
                Save : attrs['onSave'],
                Undo : attrs['onUndo'],
                Print : attrs['onPrint'],
                Setting : attrs['onSetting'],
                Export : attrs['onExport'],
                Import : attrs['onImport']
            };
            scope.$applyAsync();
        }
    }

})();