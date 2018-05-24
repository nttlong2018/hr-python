(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('hcsBreadcumb', breadcumb);

    breadcumb.$inject = ['templateService'];
    
    function breadcumb(templateService) {
        /*                                                         */
        /* ==================== Delegate - START ==================*/
        /*                                                         */
        /* Hide dropdown filter when click outside */
        $(document).mouseup(function (e) {
            var container = $("#dropdownFunction");
            if (e.target.classList[0] != 'hcs-admin-system-function-active') {
                if (!container.is(e.target) && container.has(e.target).length === 0)
                    container.hide();
                if ($('#dropdownFunction').hasClass('show'))
                    $('#dropdownFunction').removeClass('show');
            } else if ($('#dropdownFunction').hasClass('show')) {
                container.hide();
            } else
                container.show();
        });

        /*                                                         */
        /* ==================== Delegate - END ====================*/
        /*                                                         */

        // Usage:
        //     <hcs-breadcumb></hcs-breadcumb>
        // Creates:
        // 
        var directive = {
            link: link,
            scope: {
                listFunction: '=data',
                currentFunction: '=function'
            },
            templateUrl: templateService.getTemplatePath('breadcumb'),
            restrict: 'EA'
        };
        return directive;

        function link($scope, element, attrs) {
            $scope.search;
            $scope.onClickFunctionLeftMenu = templateService.onClickFunctionLeftMenu;
            $scope.onClickBreadCumbDropdownMenu = templateService.onClickBreadCumbDropdownMenu;
            $scope.onClickHideLeftMenufunction = templateService.onClickHideLeftMenufunction;
        }
    }

})();