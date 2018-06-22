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
                currentFunction: '=function',
                previousPage: '&',
                formPage: '@'
            },
            templateUrl: templateService.getTemplatePath('breadcumb'),
            restrict: 'EA'
        };
        return directive;

        function link($scope, element, attrs) {
            $scope.search;
            $scope.onClickFunctionLeftMenu = onClickFunctionLeftMenu;
            $scope.onClickBreadCumbDropdownMenu = templateService.onClickBreadCumbDropdownMenu;
            $scope.onClickHideLeftMenufunction = templateService.onClickHideLeftMenufunction;

            function _selectedMenu(function_id) {
                /* Inactive present function*/
                $('.hcs-system-admin-menu-contain ul li a.hcs-admin-system-selected').removeClass('hcs-admin-system-selected');
                $('.hcs-system-admin-menu-contain ul li.hcs-admin-system-selected').removeClass('hcs-admin-system-selected');

                $('#hcs-admin-system-panel-content div.in').removeClass('in');
                $('#hcs-admin-system-panel-content div.active').removeClass('active');

                /* Active present tab function*/
                $('#' + function_id).addClass('in');
                $('#' + function_id).addClass('active');

                /*Active present function on left menu*/
                $('#admin-system-' + function_id).addClass('hcs-admin-system-selected');
            }

            function onClickFunctionLeftMenu(f, event) {
                _selectedMenu(f.function_id)
                if ($scope["selectedUrl"]) {
                    $scope["selectedUrl"] = f.url;
                    //$parse($scope["selectedUrl"]).assign($scope.$parent, f.url);
                }
                var $his = $scope.$root.$history.data();
                window.location.href = "#page=" + $his.page + "&f=" + f.function_id;
            }

            $scope.$root.$history.change(function () {
                window.setTimeout(function () {
                    var $his = $scope.$root.$history.data();
                    if ($his.page && $his.f) {
                        _selectedMenu($his.f);
                    } else {
                        _selectedMenu($scope.listFunction[0].function_id);
                    }
                }, 100);
            });
        }
    }

})();