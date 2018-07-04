(function() {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('collapseBox', collapseBox);

    function collapseBox() {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                txtTitle: "@title",
                txtDescription: "@description"
            },
            template: '' +
              '<div class="zb-collapse-box">' +
                '<div class="zb-header">' +
                  '<div class="zb-header-content">' +
                    '<span class="zb-header-icon">' +
                      '<i class="bowtie-icon bowtie-navigate-back-circle zb-icon-up"></i>' +
                    '</span>' +
                    '<span class="zb-header-title"></span>' +
                  '</div>' +
                  '<span class="zb-header-description"></span>' +
                '</div>' +
                '<div class="zb-content" ng-transclude></div>' +
              '</div>',
            //templateUrl: "app/components/input/text/text.html",
            link: function($scope, elem, attr) {
                //var input = $(elem.find("input")[0]);
                $(elem).find(".zb-header>.zb-header-title").html($scope.txtTitle)

                var headerIcon = $(elem).find(".zb-header-icon");
                var headerTitle = $(elem).find(".zb-header-title");
                var headerDescription = $(elem).find(".zb-header-description");
                var content = $(elem).find(".zb-content");

                headerTitle.html($scope.txtTitle);

                if ($scope.txtDescription) {
                    headerDescription.html($scope.txtDescription);
                } else {
                    headerDescription.remove();
                }

                var _collapse = function() {
                    console.log(content);
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