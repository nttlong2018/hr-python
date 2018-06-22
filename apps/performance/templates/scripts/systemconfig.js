(function (scope) {

    scope.mapName = [
        { 'function_id': 'function1', 'name': 'Cấu hình hệ thống', 'url': 'systemconfig/system' },
        { 'function_id': 'function2', 'name': 'Cấu hình tài khoản', 'url': 'systemconfig/account' }
    ];

    scope.currentFunction = scope.mapName[0];

    scope.$root.$history.onChange(scope, function (data) {
        if (scope.mapName.length > 0) {
            if (data.f) {
                scope.$partialpage = data.f;
                var func = _.filter(scope.mapName, function (f) {
                    return f["function_id"] == data.f;
                });
                if (func.length > 0) {
                    scope.$partialpage = func[0].url;
                } else {
                    window.location.href = "#";
                }
            } else {
                scope.$partialpage = scope.mapName[0].url;
            }
            scope.$apply();
        } else {
            window.location.href = "#";
        }
    });
});