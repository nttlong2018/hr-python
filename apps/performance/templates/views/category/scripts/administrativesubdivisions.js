(function (scope) {
    scope.main_nation_code = null;
    scope.main_region_code = null;
    scope.$watch("main_nation_code", function (val, old) {
        if (val) {
            var tableConfig = scope.$$tableProvinceConfig;
            scope._tableProvinceData(tableConfig.iPage,
                tableConfig.iPageLength, tableConfig.orderBy,
                    tableConfig.searchText, tableConfig.fnReloadData);
        }
    }, true)

    scope.$watch("main_region_code", function (val, old) {
        if (val) {
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