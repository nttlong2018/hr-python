(function (scope) {
    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */

    scope.function = function () {
        alert('test function');
    }

    scope.onEdit = function () {
        dialog(scope).url("../pages/profile/formEdit").done(function () { });
    }

    scope.onAdd = function (p1, p2) {
        alert(p1 + ' --- ' + p2);
    }

    scope.onEditTableInfo = function () {
        dialog(scope).url("../pages/profile/formEditTableInfo").done(function () { });
    }

    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.dataSourceCombobox = {
        "gender": [
            {
                "caption": "Nam",
                "value": true
            },
            {
                "caption": "Nữ",
                "value": false
            }],
        "nation": [
            {
                "caption": "Mỹ",
                "value": "qg01"
            },
            {
                "caption": "Việt Nam",
                "value": "qg02"
            },
            {
                "caption": "Trung quốc",
                "value": "qg03"
            }],
        "folk": [
            {
                "caption": "Kinh",
                "value": "dt01"
            },
            {
                "caption": "Phong",
                "value": "dt02"
            },
            {
                "caption": "Châm",
                "value": "dt03"
            }],
        "religion": [
            {
                "caption": "Thiên chúa",
                "value": "tg01"
            },
            {
                "caption": "Hồi",
                "value": "tg02"
            },
            {
                "caption": "Phật",
                "value": "tg03"
            }],
        "culture": [
            {
                "caption": "12/12",
                "value": "hv01"
            },
            {
                "caption": "Đại học",
                "value": "hv02"
            },
            {
                "caption": "Thạc sĩ",
                "value": "hv03"
            }],
        "exercitatione": [
            {
                "caption": "Trong nước",
                "value": "htdt01"
            },
            {
                "caption": "Ngoài nước",
                "value": "htdt02"
            },
            {
                "caption": "Khác",
                "value": "htdt03"
            }],
        "educationem": [
            {
                "caption": "Trong nước",
                "value": "vh01"
            },
            {
                "caption": "Ngoài nước",
                "value": "vh02"
            },
            {
                "caption": "Khác",
                "value": "vh03"
            }],
        "married": [
            {
                "caption": "Đã kết hôn",
                "value": "hn01"
            },
            {
                "caption": "Độc thân",
                "value": "hn02"
            }],
        "city": [
            {
                "caption": "Tiền Giang",
                "value": "tp01"
            },
            {
                "caption": "TP. Hồ Chí Minh",
                "value": "tp02"
            },
            {
                "caption": "Hà Nội",
                "value": "tp03"
            },
            {
                "caption": "Mỹ tho",
                "value": "tp04"
            }],
        "district": [
            {
                "caption": "Quận 1",
                "value": "q01"
            },
            {
                "caption": "Quận 2",
                "value": "q02"
            },
            {
                "caption": "Quận 3",
                "value": "q03"
            },
            {
                "caption": "Quận 4",
                "value": "q04"
            }],
        "ward": [
            {
                "caption": "Phường 1",
                "value": "p01"
            },
            {
                "caption": "Phường 2",
                "value": "p02"
            },
            {
                "caption": "Phường 3",
                "value": "p03"
            },
            {
                "caption": "Phường 4",
                "value": "p04"
            }],
        "area": [
            {
                "caption": "Khu phố 1",
                "value": "kp01"
            },
            {
                "caption": "Khu phố 2",
                "value": "kp02"
            },
            {
                "caption": "Khu phố 3",
                "value": "kp03"
            },
            {
                "caption": "Khu phố 4",
                "value": "kp04"
            }]
    }
    scope.data = {
        "curriculum_vitae": {
            "code": "bhtien",
            "last_name": "Bùi",
            "first_name": "Hữu Tiến",
            "gender": true,
            "nation": "qg01",
            "folk": "dt01",
            "religion": "tg01"
        },
        "identity": {
            "identity_number": "025493403",
            "beginning_date": "11-07-2011",
            "city": "tp01",
            "vestige_special": "Xẹo tròn cách mắt trái 2cm",
            "tax_number": "0236519302",
        },
        "birth_page": {
            "birth_date": "04-09-1995",
            "birth_date1": "04-09-1995",
            "city": "tp01",
            "district": "q01",
            "ward": "p01",
            "area": "kp01",
        },
        "contract": {
            "temp_address":"",
            "address": "Thủ đức, TP. Hồ Chí Minh",
            "city": "tp01",
            "district": "q01",
            "ward": "p01",
            "area": "kp01",
        },
        "other": {
            "culture": "hv01",
            "exercitatione": "htdt01",
            "educationem": "vh01",
            "married": "hn01",
        },
        "list_relative": [
            {
                "name": "Nguyễn Văn Anh Vũ",
                "relation": "Anh ruột",
                "gender": "nam",
                "birthday": "01/01/1990",
                "dependent": "true",
                "host": "true",
                "createddate": "02/05/2018",
            },
            {
                "name": "Nguyễn Văn Anh Vũ",
                "relation": "Anh ruột",
                "gender": "nam",
                "birthday": "01/01/1990",
                "dependent": "true",
                "host": "true",
                "createddate": "02/05/2018",
            },
            {
                "name": "Nguyễn Văn Anh Vũ",
                "relation": "Anh ruột",
                "gender": "nam",
                "birthday": "01/01/1990",
                "dependent": "true",
                "host": "true",
                "createddate": "02/05/2018",
            },
            {
                "name": "Nguyễn Văn Anh Vũ",
                "relation": "Anh ruột",
                "gender": "nam",
                "birthday": "01/01/1990",
                "dependent": "true",
                "host": "true",
                "createddate": "02/05/2018",
            },
            {
                "name": "Nguyễn Văn Anh Vũ",
                "relation": "Anh ruột",
                "gender": "nam",
                "birthday": "01/01/1990",
                "dependent": "true",
                "host": "true",
                "createddate": "02/05/2018",
            },
            {
                "name": "Nguyễn Văn Anh Vũ",
                "relation": "Anh ruột",
                "gender": "nam",
                "birthday": "01/01/1990",
                "dependent": "true",
                "host": "true",
                "createddate": "02/05/2018",
            },
            {
                "name": "Nguyễn Văn Anh Vũ",
                "relation": "Anh ruột",
                "gender": "nam",
                "birthday": "01/01/1990",
                "dependent": "true",
                "host": "true",
                "createddate": "02/05/2018",
            }
        ]
    };
    /*                                                         */
    /* ==================== Property Scope - END ==============*/
    /*                                                         */

    /*                                                         */
    /* ==================== Object Scope - START ==============*/
    /*                                                         */
    scope.handleData = null;
    /*                                                         */
    /* ==================== Object Scope -END =================*/
    /*                                                         */

    /*                                                         */
    /* ==================== Delegate - START ==================*/
    /*                                                         */

    /*                                                         */
    /* ==================== Delegate - END ====================*/
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
            { 'function': 'function1', 'name': 'Thông tin chung' },
            { 'function': 'function2', 'name': 'Phúc lợi' },
            { 'function': 'function3', 'name': 'Kiến thức' },
            { 'function': 'function4', 'name': 'Khen thưởng - kỷ luật' },
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