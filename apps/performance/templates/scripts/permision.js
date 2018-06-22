(function (scope) {
    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    /*                                                         */
    /* ==================== Property Scope - END ==============*/
    /*                                                         */

    /*                                                         */
    /* ==================== Initialize - START=================*/
    /*                                                         */
    activate();
    init();
    /*                                                         */
    /* ==================== Initialize - END ==================*/
    /*                                                         */

    /*                                                                                          */
    /* ===============================  Implementation - START  ================================*/
    /*                                                                                          */

    /* Object handle data */
    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName = [
            { 'function_id': 'function1', 'name': 'Định nghĩa vùng dữ liệu', 'url': 'permission/domain' },
            { 'function_id': 'function2', 'name': 'Người dùng', 'url': 'permission/user' },
            { 'function_id': 'function3', 'name': 'Nhóm người dùng', 'url': 'permission/usergroup' },
            { 'function_id': 'function4', 'name': 'Phân quyền tính năng', 'url': 'permission/function' }
        ];

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

    /* Initialize Data */
    function activate() {

    }

    function init() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
    }

    /*                                                                                          */
    /* ===============================  Implementation - END  ==================================*/
    /*                                                                                          */

    scope.$root.$history.onChange(scope, function (data) {
        if (scope.mapName.length > 0) {
            if (data.f) {
                scope.$partialpage = data.f;
                var func = _.filter(scope.mapName, function (f) {
                    return f["function_id"] == data.f;
                });
                if (func.length > 0) {
                    set_function_id(func[0].function_id);
                    scope.$partialpage = func[0].url;
                } else {
                    set_function_id(HOMEPAGE_ID);
                    window.location.href = "#";
                }
            } else {
                set_function_id(scope.mapName[0].function_id);
                scope.$partialpage = scope.mapName[0].url;
            }
            scope.$apply();
        } else {
            set_function_id(HOMEPAGE_ID);
            window.location.href = "#";
        }
    });
});