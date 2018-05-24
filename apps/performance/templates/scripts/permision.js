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

    /* Mock data */
    var obj1 = [
        {
        'state': "",
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': "",
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': "",
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': "",
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': "",
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': "",
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': "",
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    },
    {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'description': 'Vùng dữ liệu dành riêng cho nhà quản trị hệ thống',
        'permision': 'Toàn quyền',
        'createdate': '02/05/2018'
    }
    ];
    
    scope.mock1 = obj1;
    
    scope.testFunction = function (model, event) {
        $("#tablePermision tbody tr.hcs-selected-row").removeClass("hcs-selected-row");
        $(event.target).parent().addClass("hcs-selected-row");
    }

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
            { 'function_id': 'function4', 'name': 'Phân quyền tính năng', 'url': 'permission/permission' },
            { 'function_id': 'function5', 'name': 'Nhóm người dùng 1' },
            { 'function_id': 'function6', 'name': 'Nhóm người dùng 2' },
            { 'function_id': 'function7', 'name': 'Nhóm người dùng 3' },
            { 'function_id': 'function8', 'name': 'Nhóm người dùng 4' },
            { 'function_id': 'function9', 'name': 'Nhóm người dùng 5' },
            { 'function_id': 'function10', 'name': 'Nhóm người dùng 6' },
            { 'function_id': 'function11', 'name': 'Nhóm người dùng 7' }
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

    scope.$root.$history.change(function (data) {
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