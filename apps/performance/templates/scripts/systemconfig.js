(function (scope) {

    scope.mapName = _.filter(scope.$root.$function_list, function (f) {
        return f.level_code.includes(scope.$root.currentFunction.function_id)
            && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
    });

    scope.currentFunction = scope.mapName[0];

    scope.$root.$history.onChange(scope, function (data) {
        if (scope.mapName.length > 0) {
            if (data.f) {
                scope.$partialpage = _.filter(scope.$root.$functions, function (f) {
                    return f.function_id = data.f
                })[0].url;
                var func = _.filter(scope.mapName, function (f) {
                    return f["function_id"] == data.f;
                });
                if (func.length > 0) {
                    scope.$partialpage = func[0].url;
                    scope.currentFunction = func[0];
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