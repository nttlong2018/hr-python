(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('navTabs', ["$compile", "$timeout", navTabs]);
    //.directive('tabContent', ["$compile", "$timeout", tabContent]);

    function navTabs($compile, $timeout) {
        return {
            restrict: 'E',
            replace: true,
            transclude: {
                "tabContent": "?tabContent"
            },
            template: `
            <div class="zb-nav-tabs">
                <ul class="zb-navbar"></ul>
                <div class="zb-tab-container" ng-transclude="tabContent"></div>
            </div>
            `,
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr, ctrls, $transclude) {
                var config = {
                    height: attr["height"],
                    minHeight: attr["minHeight"],
                    maxHeight: attr["maxHeight"]
                }
                var tabContainer = $(elem).find(".zb-tab-container");
                tabContainer.css("overflow", "auto");
                if (config.height) {
                    tabContainer.css("height", config.height);
                }
                if (config.minHeight) {
                    tabContainer.css("min-height", config.minHeight);
                }
                if (config.maxHeight) {
                    tabContainer.css("max-height", config.maxHeight);
                }

                //var htmlTransclude = $transclude();
                var tabContents = $(elem).find(".zb-tab-container>tab-content");
                console.log(tabContents);
                //Kiểm tra đã có tab được active chưa, nếu chưa mặc định chọn tab đầu tiên
                var hasActive = false;
                $.each(tabContents, function (i, v) {
                    if (v.tagName && v.tagName.toLocaleLowerCase() === "tab-content") {
                        var name = $(v).attr("name");
                        var title = ($(v).attr("title")) ? $(v).attr("title") : name;
                        var active = ($(v).attr("active") && $(v).attr("active") === "true") ? true : false;
                        var onSelect = ($(v).attr("select")) ? ($(v).attr("select")) : null;

                        if (active) hasActive = true;
                        if (name && title) {
                            var nav = '<li for="{0}" class="{2}" {3}><span>{1}</span></li>'
                            nav = nav.replace("{0}", name).replace("{1}", title)
                                .replace("{2}", active ? 'zb-active' : '')
                                .replace("{3}", onSelect ? "select='" + onSelect + "'" : '');
                            $(elem).find("ul.zb-navbar").append(nav);
                        }
                    }
                });

                $(elem).find("div.zb-tab-container>tab-content").addClass('zb-inactive');
                if (!hasActive) {
                    $($(elem).find("ul.zb-navbar>li")[0]).addClass('zb-active');
                    $($(elem).find("div.zb-tab-container>tab-content")[0]).removeClass('zb-inactive');
                } else {
                    $($(elem).find("div.zb-tab-container>tab-content[active]")[0]).removeClass('zb-inactive');
                }
                $(elem).find(">ul.zb-navbar>li").click(function () {
                    var me = $(this);
                    if (!me.hasClass("zb-active")) {
                        $(elem).find(">ul.zb-navbar>li").removeClass("zb-active");
                        me.addClass("zb-active");
                        $(elem).find("div.zb-tab-container>tab-content").addClass("zb-inactive");
                        $(elem).find("div.zb-tab-container>tab-content[name=" + me.attr("for") + "]").removeClass("zb-inactive");
                    }
                    if (me.attr("select") && angular.isFunction($scope.$eval(me.attr("select")))) {
                        ($scope.$eval(me.attr("select")))();
                    }
                });
            }
        };
    }
})();