(function (scope) {
    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.gender = [{ 'caption': 'Nguyễn Văn B', 'value': true }, { 'caption': 'Trần Thị A', 'value': false}]
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

    /**
     * Mock data
     */
    scope.tableData = [
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
    ];

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