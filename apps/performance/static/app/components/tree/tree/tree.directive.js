(function() {
    'use strict';

    angular.module('ZebraApp.components.trees')
        .directive('treeData', ["$parse", treeData]);

    /** @ngInject */
    function treeData($parse) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                source: "=",
                displayField: "@",
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
                checkAll: "="
            },
            /*
                @: lấy giá trị trên attrs,
                =: function hoặc data trên parent scope (twoway binding)
                &:function hoặc data trên parent scope (oneway binding)
            */
            templateUrl: "../performance/static/app/components/tree/tree/tree.html",
            link: function($scope, elem, attr) {
                compileTree($scope, elem, attr, $parse);
            }
        };
    }


    function compileTree($scope, elem, attr, $parse) {
        console.log($scope);
        var _tree = null;

        function _initLayout() {

            var _selectedNodes = [];
            var _curentNode = {}
            var _dataSource = [];
            var _selectedRootNodes = [];
            //var $isFirstTime = true;

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
                var selDatas = $.map($tree.getSelectedNodes(), function (node) {
                    return node.data;
                });
                _selectedNodes = selDatas;

                // Get a list of all selected TOP nodes
                var selRootDatas = $.map($tree.getSelectedNodes(true), function (node) {
                    return node.data;
                });
                _selectedRootNodes = selRootDatas;

                _setSelectedNodes(_selectedNodes, _selectedRootNodes);
            };

            var _dataSourceTree = _getDataTree($scope.source, $scope.displayField,
                $scope.parentField, $scope.keyField, $scope.parentValue, $scope.checkedField);

            if (_tree) {
                _tree.reload(_dataSourceTree)
            } else {
                //elem.find("#tree").empty();
                elem.find("#tree").fancytree({
                    extensions: ["filter"],
                    quicksearch: true,
                    checkbox: $scope.multiSelect,
                    selectMode: $scope.selectMode, // 1 (radiobutton: single-selection), 2 (multi-selection) , 3 (hierarchical multi-selection)
                    icon: false, //hide icon => hide counter
                    source: [],
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
                    //select a node
                    activate: function (event, data) {
                        _setCurrentNode(data.node.data);
                    },
                    // lazyLoad: function(event, data) {
                    //     console.log("lazyLoad", event, data);
                    //     //data.result = { url: "ajax-sub2.json" }
                    //     data.result = [ {"title": "New child 1"}, {"title": "New child 2"} ];
                    // },
                    select: function (event, data) {
                        _setSelectedOnInit(data.tree);
                    }
                    // }).on("keydown", function(e){
                    //  var c = String.fromCharCode(e.which);
                    //  if( c === "F" && e.ctrlKey ) {
                    //      elem.find("input#txtSearch").focus();
                    //  }
                });
                var _tree = elem.find("#tree").fancytree("getTree");

                _setSelectedOnInit(_tree);

                setTimeout(function () {
                    _tree.reload(_dataSourceTree);
                }, 100);

                console.log("_DATASOURCETREE", _dataSourceTree, _tree);
                console.log($scope)
                var existsWatchSelectAll = false;
                if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                    existsWatchSelectAll = _.filter($scope.$$watchers, function (f) {
                        return f.exp == "checkAll"
                    }).length > 0;
                }
                if (!existsWatchSelectAll) {
                    $scope.$watch("checkAll", function (val, old) {
                        if (val == true) {
                            elem.find("#tree").fancytree("getTree").visit(function (node) {
                                node.setSelected(true);
                            });
                        } else {
                            elem.find("#tree").fancytree("getTree").visit(function (node) {
                                node.setSelected(false);
                            });
                        }
                    });
                }


                // elem.find("button#btnResetSearch").click(function(e) {
                //     elem.find("input#txtSearch").val("");
                //     $("span#matches").text("");
                //     _tree.clearFilter();
                // }).attr("disabled", true);

                $scope.searchText = "";
                var existsWatchSearchText = false;
                if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                    existsWatchSearchText = _.filter($scope.$$watchers, function (f) {
                        return f.exp == "searchText"
                    }).length > 0;
                }
                if (!existsWatchSearchText) {
                    $scope.$watch("searchText", function (val, oVal) {
                        console.log("searchText", val)
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
            }
        }

        $scope.$watch("source", function (val, old) {
            console.log("scope.$watch(source)", val);
            _initLayout();
        }, true);
    }

    function _convertTree(_parentNodes, _dataInput, _displayField, _parentField, _keyField, _checkedField, _dataOutput) {
        if (!_dataOutput) _dataOutput = [];
        $.each(_parentNodes, function (i, v) {
            //Xóa item hiện tại khỏi danh sách dataInput
            var currIdx = _dataInput.indexOf(v);
            if (currIdx > -1) {
                _dataInput.splice(currIdx, 1);
            }
            //Tạo tree node data
            var item = {
                data: v,
                //key: v[_dataKeyField],
                title: v[_displayField],
                expanded: true
            } //Danh sách node con của item hiện tại
            if (_checkedField && v[_checkedField] == true) {
                item.selected = true;
            }
            var childrens = _.filter(_dataInput, function (f) {
                return f[_parentField] == v[_keyField];
            });
            if (childrens.length > 0) {
                item.children = [];
                _convertTree(childrens, _dataInput, _displayField, _parentField, _keyField, _checkedField, item.children);
            }
            console.log(_dataOutput);
            _dataOutput.push(item);
        });
        return _dataOutput;
    }

    function _getDataTree(_dataSource, _displayField, _parentField, _keyField, _parentValue, _checkedField) {
        //Tắt ánh xạ với dữ liệu ban đầu
        var _dataInput = JSON.parse(JSON.stringify(_dataSource));
        if (Array.isArray(_dataInput) && _dataInput.length > 0) {
            var _rootNodes = _.filter(_dataInput, function (f) {
                if (_parentValue) {
                    var _typeParentValue = typeof (_parentValue);
                    if (_typeParentValue == "string") {
                        return f[_keyField] == _parentValue;
                    } else {
                        console.log("ARR:", Array.isArray(_parentValue), _parentValue)
                        if (Array.isArray(_parentValue)) {
                            return (_parentValue.indexOf(f[_keyField]) > -1);
                        }
                        return [];
                    }
                } else {
                    return f[_parentField] == null;
                }
            });
            console.log(_rootNodes)
            var _dataOutput = [];
            _dataOutput = _convertTree(_rootNodes, _dataInput, _displayField, _parentField, _keyField, _checkedField, _dataOutput);
            console.log("_DATAOUTPUT", _dataOutput);
            return _dataOutput;
        } else {
            return [];
        }
    }
})();