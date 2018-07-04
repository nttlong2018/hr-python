(function (scope) {
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    activate();
    init();

    scope.displayDetail = false;
    scope.previousPage = previousPage;

    /* Object handle data */
    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName = [
            { 'function_id': 'function1', 'name': 'Thông tin chung', 'url': 'departments/form/common' },
            { 'function_id': 'function2', 'name': 'Chức năng', 'url': 'departments/form/function' },
            { 'function_id': 'function3', 'name': 'Nhiệm vụ', 'url': 'departments/form/question' },
            { 'function_id': 'function4', 'name': 'Lương - thưởng', 'url': 'departments/form/salary' },
            { 'function_id': 'function5', 'name': 'Thông tin kinh doanh', 'url': 'departments/form/business' },
            { 'function_id': 'function6', 'name': 'Đăng ký mẫu dấu', 'url': 'departments/form/sample' },
            { 'function_id': 'function7', 'name': 'Hội đồng quản trị', 'url': 'departments/form/council' },
            { 'function_id': 'function8', 'name': 'Ban kiểm soát', 'url': 'departments/form/control' },
            { 'function_id': 'function9', 'name': 'Theo dõi thay đỗi', 'url': 'departments/form/tracking' }
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

    function previousPage() {
        scope.displayDetail = false;
    }

    scope.changePage = function () {
        scope.displayDetail = true;
    }

    scope.$root.$history.onChange(scope, function (data) {
        if (scope.mapName.length > 0) {
            if (data.f) {
                scope.$partialpage = data.f;
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