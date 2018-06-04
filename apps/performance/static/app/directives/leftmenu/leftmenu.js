(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('hcsLeftMenu', leftmenu);

    leftmenu.$inject = ['templateService'];
    
    function leftmenu(templateService) {
        $(window).resize(function () {
            var height = $(window).height() - $('.hcs-home-page-top-bar').height()
                - $('#hcs-admin-system-heading').height()
                - $('.hcs-home-portal-footer').height();
            if ($(window).width() < 600) {
                $('.hcs-system-admin-menu-contain').height(75);
            } else {
                $('.hcs-system-admin-menu-contain').height(height);
            }
        });
        // Usage:
        //     <hcs-left-menu></hcs-left-menu>
        // Creates:
        // 
        var directive = {
            link: link,
            scope: {
                listFunction: '=data',
                displayAvatar: '=avatar',
                imageSrc: '=src'
            },
            templateUrl: '../argo/static/app/directives/leftmenu/leftmenu.html',
            restrict: 'EA'
        };
        return directive;

        function link($scope, element, attrs) {
            $scope.onClickFunctionLeftMenu = templateService.onClickFunctionLeftMenu;
            element.ready(function () {
                setHeight();
            })
        }

        function setHeight() {
            var height = $(window).height() - $('.hcs-home-page-top-bar').height()
                - $('#hcs-admin-system-heading').height()
                - $('.hcs-home-portal-footer').height();
            if ($(window).width() < 600) {
                $('.hcs-system-admin-menu-contain').height(75);
            } else {
                $('.hcs-system-admin-menu-contain').height(height);
            }
        }
    }

})();