(function (scope) {
    //("===============BEGIN TABLE==================")
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = {
        "dd_code": "Mã vùng dữ liệu",
        "dd_name": "Tên vùng vùng dữ liệu",
        "description": "Mô tả chi tiết",
        "access_mode": "Phạm vi truy cập",
        "created_on": "Thời điểm tạo"
    }
    //Dữ liệu cho table
    scope.tableSource = [];
    scope.onSelectTableRow = pressEnter;
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = null;
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.getTableData = getTableData;
    scope.tableSearchText = '';
    scope.onEdit = onEdit;
    scope.onAdd = onAdd;

    /**
     * Hàm mở form chỉnh sửa
     */
    function onEdit() {
        openDialog('Chỉnh sửa người dùng', '../pages/permission/form/editUser', function () { });
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        openDialog('Thêm mới người dùng', '../pages/permission/form/addUser', function () { });
    }

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     */
    function openDialog(title, path, callback) {
        if ($('#myModal').length == 0) {
            scope.headerTitle = title;
            dialog(scope).url(path).done(function () {
                callback(); 
            });
        }
    }

    //Event enter để mở form chỉnh sửa, hoặc tạo mới khi chưa chọn dòng
    $(document).keypress(function (e) {
        if (e.keyCode == '13') {
            if (scope.currentItem == null)
                scope.onAdd();
            else
                scope.onEdit();
        }
    })

    function getTableData() {
        console.log("currentItem", scope.currentItem);
        console.log("selectedItems", scope.selectedItems);
    }

    function pressEnter($row) {
        scope.onEdit();
    }

    function _tableData() {
        services.api("${get_api_key('app_main.api.HCSSYS_DataDomain/get_list')}")
            .data({
                //parameter at here
            })
            .done()
            .then(function (res) {
                scope.tableSource = res;
                scope.$apply();
            })
    }
    
    //("===============INIT==================")
    _tableData();
    //("===============END TABLE==================")

    //("============BEGIN TREE====================");

    var $scope = scope;
    $scope.departments = [];
    setTimeout(function () {
        $scope.departments = _departments();
        $scope.$applyAsync();
    }, 1000)
    
    $scope.selectTreeNode = function (node) {
        console.log("APP.JS -> $scope.selectTreeNode", node);
    }
    $scope.getTreeData = function () {
        console.log("CURRENT NODE ->", $scope.treeCurrentNode);
        console.log("SELECTED NODE ->", $scope.treeSelectedNodes);
        console.log("SELECTED ROOT NODE ->", $scope.treeSelectedRootNodes);
    }
    $scope.treeCurrentNode = {};
    $scope.treeSelectedNodes = [];
    $scope.treeSelectedRootNodes = [];
    $scope.treeCheckAll = false;

    function _departments() {
        return [
            {
                department_code: "lv",
                department_name: "Công ty cổ phần Tin học lạc Việt",
                parent_code: null
            },
            {
                department_code: "hcs",
                department_name: "Trung tâm HCS",
                parent_code: "lv"
            },
            {
                department_code: "hcs_dev",
                department_name: "DEV - Trung tâm HCS",
                parent_code: "hcs",
                is_selected: true,
            },
            {
                department_code: "hcs_ic",
                department_name: "IC - Trung tâm HCS",
                parent_code: "hcs"
            },
            {
                department_code: "hcs_cs",
                department_name: "CS - Trung tâm HCS",
                parent_code: "hcs"
            },
            {
                department_code: "erp",
                department_name: "Trung tâm ERP",
                parent_code: "lv"
            },
            {
                department_code: "erp_dev",
                department_name: "DEV - Trung tâm ERP",
                parent_code: "erp"
            },
            {
                department_code: "erp_ic",
                department_name: "IC - Trung tâm ERP",
                parent_code: "erp"
            },
            {
                department_code: "erp_cs",
                department_name: "CS - Trung tâm ERP",
                parent_code: "erp"
            },
        ]
    }

        //("============END TREE=================");
});