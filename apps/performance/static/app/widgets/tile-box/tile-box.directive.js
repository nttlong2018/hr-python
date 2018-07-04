(function() {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('tileBox', collapseBox);

    function collapseBox() {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                txtTitle: "@title",
                txtDescription: "@description",
                txtNumber: "@number",
                iWidth: "@width"
            },
            template: `
                <div class="zb-tile-box zb-tile-box-w{{iWidth ? iWidth : 1}}">
                    <div class="zb-tile-header">
                        <span class="zb-tile-header-left">{{txtTitle}}</span>
                        <span class="zb-tile-header-right">({{txtNumber}})</span>
                    </div>
                    <div class="zb-tile-content">
                        <p class="zb-tile-content-description">{{txtDescription}}</p>
                    </div>
                </div>
            `,
            //templateUrl: "app/components/input/text/text.html",
            link: function($scope, elem, attr) {
                var header = $(elem).find(".zb-tile-header");
                var headerTitle = $(elem).find(".zb-tile-header-left");
                var headerNumber = $(elem).find(".zb-tile-header-right");
                var contentDescription = $(elem).find(".zb-tile-content-description");

                if (!$scope.txtTitle) {
                    header.remove();
                }

                if (!$scope.txtNumber) {
                    headerNumber.remove();
                }

                if (!$scope.txtDescription) {
                    contentDescription.remove();
                }

                // var _collapse = function() {
                //     console.log(content);
                //     if (content.is(":hidden")) {
                //         headerIcon.find("i").addClass("zb-icon-up");
                //         headerIcon.find("i").removeClass("zb-icon-down");
                //     } else {
                //         headerIcon.find("i").removeClass("zb-icon-up");
                //         headerIcon.find("i").addClass("zb-icon-down");
                //     }
                //     var toggle = content.slideToggle(300);
                // }
                // headerIcon.bind("click", _collapse);
                // headerTitle.bind("click", _collapse);
            }
        };
    }
})();