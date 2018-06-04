(function (scope, system) {
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
    var obj1 = [{
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
    var obj2 = [{
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'groupcode': 'Nhóm quản trị hệ thống',
        'isAdmin': true,
        'isLock': '',
        'managefrom': 0,
        'manageto': 0,
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'groupcode': 'Nhóm quản trị hệ thống',
        'isAdmin': true,
        'isLock': '',
        'managefrom': 0,
        'manageto': 0,
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'groupcode': 'Nhóm quản trị hệ thống',
        'isAdmin': true,
        'isLock': '',
        'managefrom': 0,
        'manageto': 0,
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'groupcode': 'Nhóm quản trị hệ thống',
        'isAdmin': true,
        'isLock': '',
        'managefrom': 0,
        'manageto': 0,
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'groupcode': 'Nhóm quản trị hệ thống',
        'isAdmin': true,
        'isLock': '',
        'managefrom': 0,
        'manageto': 0,
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'groupcode': 'Nhóm quản trị hệ thống',
        'isAdmin': true,
        'isLock': '',
        'managefrom': 0,
        'manageto': 0,
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'groupcode': 'Nhóm quản trị hệ thống',
        'isAdmin': true,
        'isLock': '',
        'managefrom': 0,
        'manageto': 0,
        'createdate': '02/05/2018'
    }, {
        'state': true,
        'code': 'DD001',
        'codename': 'Quản trị hệ thống',
        'groupcode': 'Nhóm quản trị hệ thống',
        'isAdmin': true,
        'isLock': '',
        'managefrom': 0,
        'manageto': 0,
        'createdate': '02/05/2018'
        }, {
            'state': true,
            'code': 'DD001',
            'codename': 'Quản trị hệ thống',
            'groupcode': 'Nhóm quản trị hệ thống',
            'isAdmin': true,
            'isLock': '',
            'managefrom': 0,
            'manageto': 0,
            'createdate': '02/05/2018'
        }
    ];
    scope.mock1 = obj1;
    scope.mock2 = obj2;
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
            { 'function': 'function1', 'name': 'Định nghĩa vùng dữ liệu' },
            { 'function': 'function2', 'name': 'Người dùng' },
            { 'function': 'function3', 'name': 'Nhóm người dùng' },
            { 'function': 'function4', 'name': 'Phân quyền tính năng' },
            { 'function': 'function5', 'name': 'Nhóm người dùng 1' },
            { 'function': 'function6', 'name': 'Nhóm người dùng 2' },
            { 'function': 'function7', 'name': 'Nhóm người dùng 3' },
            { 'function': 'function8', 'name': 'Nhóm người dùng 4' },
            { 'function': 'function9', 'name': 'Nhóm người dùng 5' },
            { 'function': 'function10', 'name': 'Nhóm người dùng 6' },
            { 'function': 'function11', 'name': 'Nhóm người dùng 7' }
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
});