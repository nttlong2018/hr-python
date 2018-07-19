(function() {
    'use strict';

    angular.module('ZebraApp.components.trees')
        .directive('treeTable', ["$parse", "$getDataTree", treeTable]);

    /** @ngInject */
    function treeTable($parse, $getDataTree) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                source: "=",
                displayField: "@",
                displayName: "@",
                parentField: "@",
                parentValue: "=",
                keyField: "@",
                checkedField: "@",
                multiSelect: "=",
                selectMode: "=",
                onSelect: "=",
                currentNode: "=",
                selectedNodes: "=",
                selectedRootNodes: "=",
                searchText: "=",
                //checkAll: "=",
                disabled: "=",
                fields: "="
            },
            templateUrl: "app/components/tree/tree-table/tree-table.html",
            link: function($scope, elem, attr) {
                compileTree($scope, elem, attr, $parse, $getDataTree);
            }
        };
    }

    function fixedTable(elem) {
        $.each($(elem).find(".fixed"), function(i, v) {
            $(v).addClass($(v).closest("div").attr("id"));
        });

        var scroll_table_div_id = "scrolling_table";
        $(elem).scroll(function() {
            var me = this;
            var translate_y = "translate(0," + me.scrollTop + "px)";
            var translate_x = "translate(" + me.scrollLeft + "px,0px)";
            var translate_xy = "translate(" + me.scrollLeft + "px," + me.scrollTop + "px)";

            $.each($(elem).find("." + scroll_table_div_id + ".freeze_horizontal"), function(i, v) {
                $(v).css({
                    "webkit-transform": translate_x,
                    "transform": translate_x,
                });
            });

            $.each($(elem).find("." + scroll_table_div_id + ".freeze_vertical"), function(i, v) {
                $(v).css({
                    "webkit-transform": translate_y,
                    "transform": translate_y,
                });
            });

            $.each($(elem).find("." + scroll_table_div_id + ".freeze"), function(i, v) {
                $(v).css({
                    "webkit-transform": translate_xy,
                    "transform": translate_xy,
                });
            });
        });
        // setTableBody();
        // $(window).resize(setTableBody);
        // $(".zb-tree-table-body").scroll(function() {
        //     var scrollLeft = $(this).scrollLeft();
        //     $(".zb-tree-table-header").css({ left: -1 * scrollLeft });
        // });

        // function setTableBody() {
        //     $(".zb-tree-table-body").height($(".zb-tree-table").height() - $(".zb-tree-table-header").height());
        // }
    }

    function compileTree($scope, elem, attr, $parse, $getDataTree) {
        var _tree = null;

        function _initLayout() {
            if (!$scope.hasOwnProperty("checkAll")) {
                $scope.checkAll = false;
                $scope.$applyAsync();
            }

            var _selectedNodes = [];
            var _curentNode = {}
            var _dataSource = [];
            var _selectedRootNodes = [];

            if (!$scope.multiSelect) $scope.multiSelect = false;
            if (!$scope.selectMode) $scope.selectMode = 1;

            function _setCurrentNode(nodeData) {
                _curentNode = nodeData;
                $scope.currentNode = _curentNode;
                $scope.$applyAsync();
                if ($scope.onSelect && angular.isFunction($scope.onSelect)) {
                    $scope.onSelect(_curentNode);
                }
            }

            function _setSelectedNodes(selectedNodes, selectedRootNodes) {
                $scope.selectedNodes = selectedNodes;
                $scope.selectedRootNodes = selectedRootNodes;
                $scope.$applyAsync();
                // console.log("selectedNodes:", selectedNodes);
                // console.log("selectedRootNodes:", selectedRootNodes);
            }

            function _setSelectedOnInit($tree) {
                // Get a list of all selected nodes, and convert to a key array:
                var selDatas = $.map($tree.getSelectedNodes(), function(node) {
                    return node.data;
                });
                _selectedNodes = selDatas;
                // Get a list of all selected TOP nodes
                var selRootDatas = $.map($tree.getSelectedNodes(true), function(node) {
                    return node.data;
                });
                _selectedRootNodes = selRootDatas;
                _setSelectedNodes(_selectedNodes, _selectedRootNodes);
            };

            // 1 (radiobutton: single-selection), 2 (multi-selection) , 3 (hierarchical multi-selection)
            if (!$scope.selectMode) {
                $scope.selectMode = 1;
            }

            var _dataSourceTree = $getDataTree($scope);
            if (_tree) {
                _tree.reload(_dataSourceTree)
            } else {
                //elem.find("#treetable").empty();
                var _tblConf = ($scope.multiSelect) ?
                    {
                        indentation: 20, // indent 20px per node level
                        nodeColumnIdx: 1, // render the node title into the 2nd column
                        checkboxColumnIdx: 0 // render the checkboxes into the 1st column
                    } :
                    {
                        indentation: 20, // indent 20px per node level
                        nodeColumnIdx: 0, // render the node title into the 2nd column
                    };

                elem.find("#treetable").fancytree({
                    extensions: ["filter", "table"],
                    table: _tblConf,
                    quicksearch: true,
                    checkbox: $scope.multiSelect,
                    selectMode: $scope.selectMode, // 1 (radiobutton: single-selection), 2 (multi-selection) , 3 (hierarchical multi-selection)
                    icon: false, //hide icon => hide counter
                    source: _dataSourceTree,
                    filter: {
                        autoApply: true, // Re-apply last filter if lazy data is loaded
                        autoExpand: true, // Expand all branches that contain matches while filtered
                        counter: false, // Show a badge with number of matching child nodes near parent icons
                        fuzzy: false, // Match single characters in order, e.g. 'fb' will match 'FooBar'
                        hideExpandedCounter: false, // Hide counter badge if parent is expanded
                        hideExpanders: false, // Hide expanders if all child nodes are hidden by filter
                        highlight: true, // Highlight matches by wrapping inside <mark> tags
                        leavesOnly: false, // Match end nodes only
                        nodata: true, // Display a 'no data' status node if result is empty
                        mode: "hide" // "dimm" : Grayout unmatched nodes (pass "hide" to remove unmatched node instead)
                    },
                    renderColumns: function(event, data) {
                        var __createFields = function(fromIdx, dataNode, $tdList) {
                            //fromIdx: 2-table with checkbox, 1-table without checkbox
                            $.each($scope.fields, function(i, v) {
                                let _fnFormatRender = null;
                                if (v.format) {
                                    var $s = v.format.split(":");
                                    if ($s[0].toLowerCase() === 'date') {
                                        //Add function render to columns
                                        //$filter('date')(date, format, timezone)
                                        _fnFormatRender = function(data) {
                                            let $r;
                                            switch ($s.length) {
                                                case 3:
                                                    $r = $filter('date')(data, $s[1], $s[2]);
                                                    break;
                                                case 2:
                                                    $r = $filter('date')(data, $s[1]);
                                                    break;
                                                default:
                                                    $r = $filter('date')(data);
                                            }
                                            return $r;
                                        }
                                    } else if ($s[0].toLowerCase() === 'number') {
                                        //Add function render to columns
                                        //$filter('number')(number, fractionSize)
                                        _fnFormatRender = function(data) {
                                            let $r;
                                            switch ($s.length) {
                                                case 2:
                                                    $r = $filter('number')(data, $s[1]);
                                                    break;
                                                default:
                                                    $r = $filter('number')(data);
                                            }
                                            return $r;
                                        }
                                    } else if ($s[0].toLowerCase() === 'currency') {
                                        //Add function render to columns
                                        //$filter('currency')(amount, symbol, fractionSize)
                                        _fnFormatRender = function(data) {
                                            let $r;
                                            switch ($s.length) {
                                                case 3:
                                                    $r = $filter('currency')(data, $s[1], $s[2]);
                                                    break;
                                                case 2:
                                                    $r = $filter('currency')(data, $s[1]);
                                                    break;
                                                default:
                                                    $r = $filter('currency')(data);
                                            }
                                            return $r;
                                        }
                                    } else if ($s[0].toLowerCase() === 'lowercase') {
                                        //Add function render to columns
                                        //$filter('lowercase')()
                                        _fnFormatRender = function(data) {
                                            return $filter('lowercase')(data);
                                        }
                                    } else if ($s[0].toLowerCase() === 'uppercase') {
                                        //Add function render to columns
                                        //$filter('uppercase')()
                                        _fnFormatRender = function(data) {
                                            return $filter('uppercase')(data);
                                        }
                                    } else if ($s[0].toLowerCase() === 'json') {
                                        //Add function render to columns
                                        //$filter('json')(object, spacing)
                                        _fnFormatRender = function(data) {
                                            let $r;
                                            switch ($s.length) {
                                                case 2:
                                                    $r = $filter('json')(data, $s[1]);
                                                    break;
                                                default:
                                                    $r = $filter('json')(data);
                                            }
                                            return $r;
                                        }
                                    } else if ($s[0].toLowerCase() === 'checkbox') {
                                        //Add function render to columns
                                        _fnFormatRender = function(data) {
                                            return (data) ? "<span class='zb-checkbox-symbol'>&#9745;</span>" : "<span class='zb-checkbox-symbol'>&#9744;</span>";
                                        }
                                    }

                                }
                                var __data = (_fnFormatRender) ? _fnFormatRender(node.data[v.data]) : node.data[v.data];
                                $tdList.eq(fromIdx + i).html(__data).addClass((v.className) ? v.className : '');
                            });
                        }

                        var node = data.node,
                            $tdList = $(node.tr).find(">td");

                        //var node = data.node, $tdList = $(node.tr).find(">td");

                        if ($scope.multiSelect) {
                            // // (index #0 is rendered by fancytree by adding the checkbox)
                            // // (index #1 is rendered by fancytree)
                            // $tdList.eq(0).addClass("zb-tree-table-checkbox")
                            // //$tdList.eq(0).addClass("zb-tree-table-content")
                            // $tdList.eq(2).text(node.key) //.addClass("alignRight");
                            // $tdList.eq(3).text(node.data["custom_name"]); //node.title
                            // $tdList.eq(4).html("<input type='checkbox' name='like' value='" + node.key + "'>");
                            $tdList.eq(0).addClass("zb-tree-table-checkbox")
                            __createFields(2, node, $tdList);
                        } else {
                            __createFields(1, node, $tdList);
                        }
                    },
                    //select a node
                    activate: function(event, data) {
                        _setCurrentNode(data.node.data);
                    },
                    // lazyLoad: function(event, data) {
                    //     console.log("lazyLoad", event, data);
                    //     //data.result = { url: "ajax-sub2.json" }
                    //     data.result = [ {"title": "New child 1"}, {"title": "New child 2"} ];
                    // },
                    select: function(event, data) {
                        _setSelectedOnInit(data.tree);
                    }
                    // }).on("keydown", function(e){
                    //  var c = String.fromCharCode(e.which);
                    //  if( c === "F" && e.ctrlKey ) {
                    //      elem.find("input#txtSearch").focus();
                    //  }
                });
                elem.find("input.zb-tree-table-checkall").unbind("change");
                elem.find("input.zb-tree-table-checkall").bind("change", function() {
                    if ($(this).prop("checked") == true) {
                        elem.find("#treetable").fancytree("getTree").visit(function(node) {
                            node.setSelected(true);
                        });
                    } else {
                        elem.find("#treetable").fancytree("getTree").visit(function(node) {
                            node.setSelected(false);
                        });
                    }
                });

                setTimeout(function() {
                    fixedTable(elem);
                }, 300);
                var _tree = elem.find("#treetable").fancytree("getTree");

                setTimeout(function() {
                    _tree.reload(_dataSourceTree);
                    _setSelectedOnInit(_tree);
                }, 100);

                // elem.find("button#btnResetSearch").click(function(e) {
                //     elem.find("input#txtSearch").val("");
                //     $("span#matches").text("");
                //     _tree.clearFilter();
                // }).attr("disabled", true);

                $scope.searchText = "";
                var existsWatchSearchText = false;
                if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                    existsWatchSearchText = _.filter($scope.$$watchers, function(f) {
                        return f.exp == "searchText"
                    }).length > 0;
                }
                if (!existsWatchSearchText) {
                    $scope.$watch("searchText", function(val, oVal) {
                        var n,
                            //tree = $.ui.fancytree.getTree(),
                            filterFunc = _tree.filterNodes, //$("#branchMode").is(":checked") ? tree.filterBranches : tree.filterNodes,
                            match = val;
                        if (val && val.trim()) {
                            n = filterFunc.call(_tree, val);
                            console.log("Found: (" + n + " matches) for ('" + val + "')");
                        } else {
                            _tree.clearFilter();
                            console.log("Found: (" + 0 + " matches) for ('" + val + "')");
                        }
                        //n = filterFunc.call(_tree, val);

                        // if (e && e.which === $.ui.keyCode.ESCAPE || $.trim(val) === "") {
                        //     $("button#btnResetSearch").click();
                        //     return;
                        // }

                        // if ($("#regex").is(":checked")) {
                        //     <!-- n = filterFunc.call(_tree, function(node) { -->
                        //     <!-- return new RegExp(match, "i").test(node.title); -->
                        //     <!-- }); -->
                        // } else {
                        //     n = filterFunc.call(_tree, match);
                        // }
                    })
                }
                //Nếu thay đổi chạy lại cây
                let _watchInits = ["multiSelect", "selectMode", "disabled"];
                let _isFirstTime = true;
                $.each(_watchInits, function(i, v) {
                    var existsWatchInit = false;
                    if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                        existsWatchInit = _.filter($scope.$$watchers, function(f) {
                            return f.exp == v
                        }).length > 0;
                    }
                    if (!existsWatchInit) {
                        $scope.$watch(v, function(val, old) {
                            //alert(v + "-" + _isFirstTime);
                            if (!_isFirstTime) {
                                _initLayout();
                            }
                        }, true);
                    }
                });
                _isFirstTime = false;
            }
        }

        $scope.$watch("source", function(val, old) {
            _initLayout();
        }, true);
    }
})();