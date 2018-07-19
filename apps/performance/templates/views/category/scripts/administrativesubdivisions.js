(function (scope) {
    scope.$parent.$parent.$parent.$watch("advancedSearch", function (val, old) {
        if (val && val.main_nation_code) {
            var tableConfig = scope.$$tableProvinceConfig;
            scope._tableProvinceData(tableConfig.iPage,
                tableConfig.iPageLength, tableConfig.orderBy,
                    tableConfig.searchText, tableConfig.fnReloadData);
        }
    }, true)

    scope.$parent.$parent.$parent.$watch("advancedSearch", function (val, old) {
        if (val && val.main_region_code) {
            var tableConfig = scope.$$tableProvinceConfig;
            scope._tableProvinceData(tableConfig.iPage,
                tableConfig.iPageLength, tableConfig.orderBy,
                tableConfig.searchText, tableConfig.fnReloadData);
        }
    }, true)

    scope.$watch("currentProvince", function (val, old) {
        if (val && Object.keys(val).length > 0) {
            var tableConfig = scope.$$tableDistrictConfig;
            scope._tableDistrictData(tableConfig.iPage,
                tableConfig.iPageLength, tableConfig.orderBy,
                    tableConfig.searchText, tableConfig.fnReloadData);
        }
    }, true)

    scope.$watch("currentDistrict", function (val, old) {
        if (val && Object.keys(val).length > 0) {
            var tableConfig = scope.$$tableWardConfig;
            scope._tableWardData(tableConfig.iPage,
                tableConfig.iPageLength, tableConfig.orderBy,
                tableConfig.searchText, tableConfig.fnReloadData);
        }
    }, true)

    scope.$watch("currentWard", function (val, old) {
        if (val && Object.keys(val).length > 0) {
            var tableConfig = scope.$$tableHamletConfig;
            scope._tableHamletData(tableConfig.iPage,
                tableConfig.iPageLength, tableConfig.orderBy,
                tableConfig.searchText, tableConfig.fnReloadData);
        }
    }, true)
});