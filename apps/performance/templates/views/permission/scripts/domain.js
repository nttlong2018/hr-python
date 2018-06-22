(function (scope) {
    //("===============BEGIN TABLE==================")
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "dd_code", "title": "${get_res('dd_code_table_title','Mã vùng dữ liệu')}"},
        { "data": "dd_name", "title": "${get_res('dd_name_table_title','Tên vùng vùng dữ liệu')}"},
        { "data": "description", "title": "${get_res('description_table_title','Mô tả chi tiết')}"},
        { "data": "display_access_mode", "title": "${get_res('display_access_mode_table_title','Phạm vi truy cập')}" },
        { "data": "created_on", "title": "${get_res('created_on_table_title','Thời điểm tạo')}", "format": "date:" + scope.$root.systemConfig.date_format }
    ];
    //
    scope.$$tableConfig = {};
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
        //setTimeout(function () {
        if (fnReloadData) {
            if (searchText) {
                _tableData(iPage, iPageLength, orderBy, searchText, function (data) {
                    fnReloadData(data);
                });
            } else {
                _tableData(iPage, iPageLength, orderBy, null, function (data) {
                    fnReloadData(data);
                });
            }
        }
        //}, 1000);
    };
    scope.onSelectTableRow = pressEnter;
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.getTableData = getTableData;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = function () { /*Do nothing*/ };
    //Mode 1: tạo mới, Mode 2: chỉnh sửa, Mode 3: sao chép
    scope.mode = 0;
    scope.onEdit = onEdit;
    scope.onAdd = onAdd;
    scope.onDelete = onDelete;
    scope.onCopy = onCopy;
    scope.onSearch = onSearch;
    scope.onExport = onExport;
    scope.onImport = onImport;
    scope._tableData = _tableData;
    scope.mapAccess_mode = [];
    //scope.getDisplayNameAccessMode = getDisplayNameAccessMode;

    /**
     * Hàm mở form chỉnh sửa
     */
    function onEdit() {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Edit_Domain','Chỉnh sửa vùng truy cập')}", 'permission/form/addDomain', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Add_New_Domain','Thêm mới vùng truy cập')}", 'permission/form/addDomain', function () { });
    }
    function onDelete() {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSSYS_DataDomain/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.SUCCESS);
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }
    }
    function onCopy() {
        if (scope.currentItem) {
            scope.mode = 3; // set mode chỉnh sửa
            openDialog("${get_res('Add_New_Domain','Thêm mới vùng truy cập')}", 'permission/form/addDomain', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }
    function onSearch(val) {
        scope.tableSearchText = scope.SearchText;
        scope.$apply();
    }
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'HCSSYS_DataDomain'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            //.setFunctionID("aaaaa")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    }
    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        var fn = {
            "button": [{ "func_name": "saveNClose", "icon": "la la-save", "name": "${get_global_res('save_and_close','Lưu & đóng')}" },
            { "func_name": "saveNNext", "icon": "la la-save", "name": "${get_global_res('save_and_next','Lưu & tiếp')}" }]
        };
        //check tồn tại của form dialog theo id
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id, fn).url(path).done(function () {
                callback();
                //Set resizable cho form dialog theo id
                $('#myModal').ready(function () {
                    $('#myModal .modal-dialog .modal-content .modal-header').on('mousedown touchstart', function (e) {
                        $('#myModal .modal-dialog').draggable();
                    }).bind('mouseup touchend', function () {
                        $('#myModal .modal-dialog').draggable('destroy');
                    });
                })
            });
        }
    }
    function getTableData() {
        console.log("currentItem", scope.currentItem);
        console.log("selectedItems", scope.selectedItems);
    }
    function pressEnter($row) {
        scope.onEdit();
    }
    //function getDisplayNameAccessMode(code) {
    //    var name = '';
    //    _.each(scope.mapAccess_mode, function (val) {
    //        if (val.value == code) {
    //            name = val.caption;
    //            return;
    //        }
    //    })
    //    return name;
    //}
    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.HCSSYS_DataDomain/get_list_with_searchtext')}")
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
                "name": "AccessDomain"
            })
            .done()
            .then(function (res) {
                delete res.language;
                delete res.list_name;
                scope.mapAccess_mode = res.values;
                console.log(res);
                scope.$applyAsync();
            })
    }
    _comboboxData();
    //("===============INIT==================")
    //_tableData();
    //("===============END TABLE==================")
});