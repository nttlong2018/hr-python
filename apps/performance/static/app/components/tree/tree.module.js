'use strict';

var app = angular.module('ZebraApp.components.trees', []);
app.factory('$getDataTree', function() {
    var _convertTree = function ($scope, _parentNode, _treeNodes, _dataInput, _displayField, _parentField, _keyField, _checkedField, _dataOutput) {
        if (!_dataOutput) _dataOutput = [];
        $.each(_treeNodes, function(i, v) {
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
            }
            if ($scope.multiSelect) {
                if ($scope.selectMode === 3 && _parentNode && _parentNode.selected) {
                    item.selected = true;
                }
                if (_checkedField && v[_checkedField] == true && !item.selected) {
                    item.selected = true;
                }
            }
            if ($scope.disabled) {
                item.unselectable = true;
            }

            var childrens = _.filter(_dataInput, function(f) {
                return f[_parentField] == v[_keyField];
            });
            if (childrens.length > 0) {
                item.children = [];
                _convertTree($scope, item, childrens, _dataInput, _displayField, _parentField, _keyField, _checkedField, item.children);
            }
            _dataOutput.push(item);
        });
        return _dataOutput;
    }

    var _getDataTree = function ($scope) {
        let _treeMode = $scope.selectMode,
            _dataSource = $scope.source,
            _displayField = $scope.displayField,
            _parentField = $scope.parentField,
            _keyField = $scope.keyField,
            _parentValue = $scope.parentValue,
            _checkedField = $scope.checkedField;

        //Tắt ánh xạ với dữ liệu ban đầu
        if (!_dataSource) return [];
        var _dataInput = JSON.parse(JSON.stringify(_dataSource));
        if (Array.isArray(_dataInput) && _dataInput.length > 0) {
            var _rootNodes = _.filter(_dataInput, function(f) {
                if (_parentValue) {
                    var _typeParentValue = typeof(_parentValue);
                    if (_typeParentValue == "string") {
                        return f[_keyField] == _parentValue;
                    } else {
                        if (Array.isArray(_parentValue)) {
                            return (_parentValue.indexOf(f[_keyField]) > -1);
                        }
                        return [];
                    }
                } else {
                    return f[_parentField] == null;
                }
            });
            var _dataOutput = [];
            _dataOutput = _convertTree($scope, null, _rootNodes, _dataInput, _displayField, _parentField, _keyField, _checkedField, _dataOutput);
            return _dataOutput;
        } else {
            return [];
        }
    }

    return _getDataTree;
});