(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('pageSidebar', ["$compile", pageSidebar]);

    function pageSidebar($compile) {
        return {
            restrict: 'E',
            replace: true,
            transclude: {
                siteMap: "?siteMap",
                advancedSearch: "?advancedSearch",
                extendToolbar: "?extendToolbar",
                content: "content"
            },
            scope: {
                fnAdd: "=onAdd",
                fnEdit: "=onEdit",
                fnDelete: "=onDelete",
                fnSave: "=onSave",
                fnImport: "=onImport",
                fnExport: "=onExport",
                fnSearchPress: "=onSearchPress",
                fnSearchChange: "=onSearchChange",
                listItem: "=source",
                keyField: "@",
                displayField: "@",
                iconField: "@",
                selectedKey: "=",
                reloadOnChange: "=",
                advancedSearch: "=",
                extendToolbar: "="
            },
            //templateUrl: "app/widgets/page-sidebar/page-sidebar.html",
            template: `
            <div class="zb-page-sidebar">
                <div class="zb-left">
                    <ul class="zb-left-ul">
                        <li ng-repeat="item in listItem" class="zb-left-li" ng-class="item[keyField]==selectedKey?'li-selected':''"      ng-click="$onSelectItem(item[keyField])">
                            <div>
                                <p class="left-icon text-center"><i class="{{item[iconField]}}"></i></p>
                                <p class="left-title text-center">{{item[displayField]}}</p>
                            </div>
                        </li>
                    </ul>
                </div>
                <div class="zb-right">
                    <div class="zb-top">
                        <div class="zb-left-content">
                            <button ng-click="toggleCollapseMenu()" class="zb-btn zb-btn-blue zb-btn-collapse">
                                <i class="bowtie-icon bowtie-menu"></i>
                            </button>
                            <div ng-transclude="siteMap" class="zb-sitemap"></div>
                        </div>
                        <div class="zb-right-content">
                            <div ng-transclude="extendToolbar" class="zb-extend-toolbar"></div>
                            <input-text-icon icon="bowtie-icon bowtie-search" icon-align="right" placeholder="" ng-model="texticon2" on-click="fnSearchPress" on-change="fnSearchChange" ng-show="fnSearchPress || fnSearchChange">
                            </input-text-icon>
                            <button ng-click="showAdvancedSearch()" class="zb-btn" ng-if="isAdvancedSearch">
                                <i class="bowtie-icon bowtie-search-filter"></i>
                            </button>
                            <button class="zb-btn zb-btn-o-green" ng-if="fnAdd" ng-click="fnAdd()">
                                <i class="bowtie-icon bowtie-math-plus"></i>
                            </button>
                            <button class="zb-btn zb-btn-o-blue" ng-if="fnEdit" ng-click="fnEdit()">
                                <i class="bowtie-icon bowtie-edit-outline"></i>
                            </button>
                            <button class="zb-btn zb-btn-o-red" ng-if="fnDelete" ng-click="fnDelete()">
                                <i class="bowtie-icon bowtie-edit-remove"></i>
                            </button>
                            <button class="zb-btn" ng-if="fnSave" ng-click="fnSave()">
                                <i class="bowtie-icon bowtie-save"></i>
                            </button>
                            <button class="zb-btn" ng-if="fnImport" ng-click="fnImport()">
                                <i class="bowtie-icon bowtie-transfer-upload"></i>
                            </button>
                            <button class="zb-btn" ng-if="fnExport" ng-click="fnExport()">
                                <i class="bowtie-icon bowtie-transfer-download"></i>
                            </button>
                        </div>
                    </div>
                    <div ng-transclude="advancedSearch" class="zb-advanced-search"></div>
                    <div class="zb-content" ng-transclude="content"></div>
                </div>
            </div>
            `,
            link: function ($scope, elem, attr, ctrls, $transclude) {
                console.log($scope)
                var left = $(elem).find(".zb-left");
                var right = $(elem).find(".zb-right");
                var rightContent = $(elem).find(".zb-right .zb-content");
                var btnCollapse = $(elem).find("#btnCollapse");

                var advancedSearch = $(elem).find(".zb-advanced-search");
                var btnAdvancedSearch = $(elem).find("#btnAdvancedSearch");

                $scope.$watch("listItem", function (v) {
                    if (!$scope.selectedKey && angular.isArray($scope.listItem) && $scope.listItem.length > 0) {
                        $scope.selectedKey = $scope.listItem[0][$scope.keyField];
                    }
                });

                $scope.isAdvancedSearch = $transclude.isSlotFilled('advancedSearch');
                $scope.showAdvancedSearch = showAdvancedSearch;
                $scope.toggleCollapseMenu = toggleCollapseMenu;
                $scope.$onSelectItem = $onSelectItem;
                $scope.$applyAsync();


                function toggleCollapseMenu() {
                    left.toggleClass("zb-hidden");
                    right.toggleClass("zb-fullscreen");
                    setTimeout(function () {
                        $(window).trigger("resize");
                    }, 300);
                }

                function showAdvancedSearch() {
                    advancedSearch.toggleClass("zb-show");
                    rightContent.toggleClass("show-advanced");
                }

                function $onSelectItem(key) {
                    $scope.selectedKey = key;

                    if ($scope.reloadOnChange) {
                        $scope.fnAdd = null;
                        $scope.fnEdit = null;
                        $scope.fnDelete = null;
                        $scope.fnSave = null;
                        $scope.fnImport = null;
                        $scope.fnExport = null;
                        $scope.fnSearchPress = null;
                        $scope.fnSearchChange = null;
                    }

                    $scope.$applyAsync();
                }
            }
        };
    }
})();