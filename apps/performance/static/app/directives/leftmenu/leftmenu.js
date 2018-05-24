(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('hcsLeftMenu', leftmenu);

    leftmenu.$inject = ['templateService', '$parse'];
    
    function leftmenu(templateService, $parse) {
        // Usage:
        //     <hcs-left-menu></hcs-left-menu>
        // Creates:
        // 
        var directive = {
            link: link,
            scope: {
                listFunction: '=data',
                displayAvatar: '=avatar',
                imageSrc: '=src',
                selectedUrl: '&selectedUrl'
            },
            templateUrl: templateService.getTemplatePath('leftmenu'),
            restrict: 'EA'
        };
        return directive;

        function link($scope, element, attrs) {
            function _selectedMenu(function_id) {
                /* Inactive present function*/
                element.find('.hcs-system-admin-menu-contain ul li a.hcs-admin-system-selected').removeClass('hcs-admin-system-selected');
                element.find('.hcs-system-admin-menu-contain ul li.hcs-admin-system-selected').removeClass('hcs-admin-system-selected');

                element.find('#hcs-admin-system-panel-content div.in').removeClass('in');
                element.find('#hcs-admin-system-panel-content div.active').removeClass('active');

                /* Active present tab function*/
                element.find('#' + function_id).addClass('in');
                element.find('#' + function_id).addClass('active');

                /*Active present function on left menu*/
                element.find('#admin-system-' + function_id).addClass('hcs-admin-system-selected');
            }

            $scope.onClickFunctionLeftMenu = function onClickFunctionLeftMenu(f, event) {
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