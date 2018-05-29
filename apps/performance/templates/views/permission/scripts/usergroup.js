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
        openDialog('Chỉnh sửa nhóm người dùng', '../pages/permission/form/addUserGroup', function () { });
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        openDialog('Thêm mới nhóm người dùng', '../pages/permission/form/addUserGroup', function () { });
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
});