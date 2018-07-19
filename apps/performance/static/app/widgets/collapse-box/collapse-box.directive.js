(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('collapseBox', collapseBox);

    function collapseBox() {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            // scope: {
            //     txtTitle: "@title",
            //     txtDescription: "@description"
            // },
            template: '' +
                '<div class="zb-collapse-box">' +
                '<div class="zb-header">' +
                '<div class="zb-header-content">' +
                '<span class="zb-header-icon">' +
                '<i class="bowtie-icon bowtie-chevron-left-light zb-icon-up"></i>' +
                /*bowtie-navigate-back-circle*/
                '</span>' +
                '<span class="zb-header-title"></span>' +
                '</div>' +
                '<span class="zb-header-description"></span>' +
                '</div>' +
                '<div class="zb-content"></div>' +
                '</div>',
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr, ctrls, $transclude) {
                var $config = {
                    txtTitle: attr["title"],
                    txtDescription: attr["description"]
                };

                var headerIcon = $(elem).find(".zb-header-icon");
                var headerTitle = $(elem).find(".zb-header-title");
                var headerDescription = $(elem).find(".zb-header-description");
                var content = $(elem).find(".zb-content");

                $transclude($scope, function (nodes) {
                    $(elem).find(".zb-content").append(nodes);;
                })

                headerTitle.html($config.txtTitle);
                headerDescription.html($config.txtDescription);
                if (!$config.txtDescription) {
                    headerDescription.remove();
                }

                var _collapse = function () {
                    if (content.is(":hidden")) {
                        headerIcon.find("i").addClass("zb-icon-up");
                        headerIcon.find("i").removeClass("zb-icon-down");
                    } else {
                        headerIcon.find("i").removeClass("zb-icon-up");
                        headerIcon.find("i").addClass("zb-icon-down");
                    }
                    var toggle = content.slideToggle(300);
                }
                headerIcon.bind("click", _collapse);
                headerTitle.bind("click", _collapse);
            }
        };
    }
})();