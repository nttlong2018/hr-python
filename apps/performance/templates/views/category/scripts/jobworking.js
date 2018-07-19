(function (scope) {
    //("===============BEGIN TABLE==================")
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "JobWCode", "title": "${get_res('jobwcode_table_header','Mã CDCV')}" },
        { "data": "JobWName", "title": "${get_res('jobwname_table_header','Tên CDCV')}" },
        { "data": "JobWDuty", "title": "${get_res('jobwduty_table_header','Trách nhiệm & Quyền hạn')}" },
        { "data": "GJWCode", "title": "${get_res('gjwcode_table_header','Nhóm chức danh CV')}" },
        { "data": "Ordinal", "title": "${get_res('ordinal_table_header','STT')}" },
        { "data": "Lock", "title": "${get_res('lock_table_header','Ngưng sd')}", "format": "checkbox" },
        { "data": "IsJobWMainStaff", "title": "${get_res('IsJobWMainStaff_table_header','Là vị trí chủ chốt')}", "format": "checkbox" },
        { "data": "ReportToJobW", "title": "${get_res('ReportToJobW_table_header','Báo cáo cho')}" },
        { "data": "InternalProcess", "title": "${get_res('InternalProcess_table_header','Quy trình nội bộ')}" },
        { "data": "CombineProcess", "title": "${get_res('CombineProcess_table_header','Quy trình phối hợp')}" },
        { "data": "Description", "title": "${get_res('Description_table_header','Mục tiêu công việc')}" },
        { "data": "JobWWork", "title": "${get_res('JobWWork_table_header','Công việc thực hiện')}" },
        { "data": "EffectDate", "title": "${get_res('EffectDate_table_header','Ngày hiệu lực')}" },
        { "data": "JobPosCode", "title": "${get_res('JobPosCode_table_header','Thuộc chức vụ/ cấp bậc')}" },
    ];
    //
    scope.$$tableConfig = {};
    //Dữ liệu cho table
    scope.tableSource = scope.$parent.$$DataJobWorkingGroup;
    scope.onSelectTableRow = pressEnter;
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = function () { /*Do nothing*/ };
    //Mode 1: tạo mới, Mode 2: chỉnh sửa, Mode 3: sao chép
    scope.mode = 0;
    scope.onEdit = onEdit;
    scope.onAdd = onAdd;
    scope.onDelete = onDelete;
    scope.onSearch = onSearch;
    scope.onReload = onReload;
    scope._tableData = _tableData;
    scope.cbbAwardType = [];

    /**
     * Hàm mở form chỉnh sửa
     */
    function onEdit() {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Detail_Award','Chi tiết hình thức khen thưởng')}", 'category/form/addJobWorking', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Detail_JobWorking','Chi tiết Chức danh công việc')}", 'category/form/addJobWorking', function () { });
    }
    function onDelete() {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSLS_Award/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }
    }

    function onSearch(val) {
        scope.tableSearchText = $('#tableAwardSearchText').val();
        scope.$applyAsync();
    }

    function onReload() {
        var tableConfig = scope.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {

        //check tồn tại của form dialog theo id
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }

    function pressEnter($row) {
        
    }

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.HCSLS_Award/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort
                })
                .done()
                .then(function (res) {
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);
                    scope.currentItem = null;
                    scope.$apply();
                })
    }

    function _comboboxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                //parameter at here
                "name": "LAwardType"
            })
            .done()
            .then(function (res) {
                delete res.language;
                delete res.list_name;
                scope.cbbAwardType = res.values;
                scope.$applyAsync();
            })
    }
    _comboboxData();

    $(document).ready(function () {
        $('#tableAwardSearchText').on('keypress', function (e) {
            var code = e.keyCode || e.which;
            if (code == 13) {
                scope.tableSearchText = $('#tableAwardSearchText').val();
                scope.$applyAsync();
            }
        });
    })

    //("===============INIT==================")
    //_tableData();
    //("===============END TABLE==================")
});