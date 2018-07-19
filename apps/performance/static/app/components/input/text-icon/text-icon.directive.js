(function () {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('inputTextIcon', ["$parse", "$compile", inputTextIcon]);

    /** @ngInject */
    function inputTextIcon($parse, $compile) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            template: '<div class="zb-form-text-icon input-group"></div>',
            //templateUrl: "app/components/input/text/text.html",
            compile: function (elem, attr) {
                const ALIGN = {
                    RIGHT: "right",
                    LEFT: "left"
                };
                var config = {};
                config.ngModel = (attr["ngModel"]) ? attr["ngModel"] : '';
                config.iconAlign = (attr["iconAlign"]) ? attr["iconAlign"].toLowerCase() : ALIGN.RIGHT;
                config.placeholder = attr["placeholder"] ? attr["placeholder"] : '';
                config.icon = (attr["icon"]) ? attr["icon"] : 'glyphicon glyphicon-search';
                config.click = (attr["onClick"]) ? attr["onClick"] : null;
                config.change = (attr["onChange"]) ? attr["onChange"] : null;

                if (attr["required"]) {
                    $(elem).wrap("<span zb-required></span>")
                }

                var sInput = '<input type="text" class="form-control" placeholder="<<placeholder>>" ng-model="<<ngModel>>"></input>';
                sInput = sInput.replace("<<placeholder>>", config.placeholder).replace("<<ngModel>>", config.ngModel);
                var sIcon = '' +
                    '<div class="input-group-btn">' +
                    '   <button class="btn btn-default"><i class="<<icon>>"></i></button>' +
                    '</div>';
                sIcon = sIcon.replace("<<icon>>", config.icon);

                if (config.iconAlign === ALIGN.LEFT) {
                    $(elem).append(sIcon).append(sInput);
                } else {
                    $(elem).append(sInput).append(sIcon);
                }
                var subLink = $compile(elem);
                return {
                    pre: function (scope, elem, attr, controller, transcludeFn) {
                        subLink(scope);
                    },
                    post: function (scope, element, attributes, controller, transcludeFn) {
                        if (config.click) {
                            var _search = function () {
                                var txtSearch = $(elem).find("input").val();
                                if (angular.isFunction((scope.$eval(config.click)))) {
                                    (scope.$eval(config.click))(txtSearch);
                                }
                            };
                            $(elem).find("button").bind("click", function () {
                                _search();
                            });
                            $(elem).find("input").keyup(function (e) {
                                if (e.which == 13) {
                                    _search();
                                }
                            });
                        }
                        if (config.change) {
                            $(elem).find("input").keyup(function () {
                                if (angular.isFunction((scope.$eval(config.change)))) {
                                    var txtSearch = $(elem).find("input").val();
                                    (scope.$eval(config.change))(txtSearch);
                                }
                            });
                        }
                    }
                }
            }

        };
    }
})();