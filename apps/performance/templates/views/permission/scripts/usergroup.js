(function (scope) {
    //("===============BEGIN TABLE==================")
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "role_code", "title": "${ get_res('role_code_table_title', 'Mã nhóm người dùng') }" },
        { "data": "role_name", "title": "${ get_res('role_name_table_title', 'Tên nhóm người dùng') }" },
        { "data": "description", "title": "${ get_res('description_table_title', 'Mô tả chi tiết') }" },
        { "data": "dd_code", "title": "${ get_res('dd_code_table_title', 'Mã vùng dữ liệu truy cập') }" },
        { "data": "stop", "title": "${ get_res('stop_table_title', 'Ngưng sử dụng') }" },
        {
            "data": "created_on",
            "title": "${ get_res('created_on_table_title', 'Thời điểm tạo') }",
            "format": "date: " + scope.$root.systemConfig.date_format
        }
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
    scope._tableData = _tableData;
    scope.$applyAsync();
    /**
     * Hàm mở form chỉnh sửa
     */
    function onEdit() {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Edit_UserGroup','Chỉnh sửa nhóm người dùng')}", 'permission/form/addUserGroup', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Add_UserGroup','Thêm mới nhóm người dùng')}", 'permission/form/addUserGroup', function () { });
    }

    function onDelete() {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.AD_Roles/delete')}")
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
            openDialog("${get_res('Add_New_UserGroup','Thêm mới nhóm người dùng')}", 'permission/form/addUserGroup', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    function onSearch() {
        scope.tableSearchText = scope.SearchText;
        scope.$applyAsync();
    }
    function onExport() {
        window.open("/excel_export");
        //services.api("/excel_export")
        //    .data({})
        //    .done()
        //    .then(function (res) {

        //    })
        //$.ajax({
        //    url: "/excel_export",
        //    contentType: 'application/json; charset=utf-8',
        //    type: 'POST',
        //    // type: 'GET',
        //    dataType: 'json',
        //    error: function (xhr, status) {
        //        alert(status);
        //    },
        //    success: function (result) {
        //        alert("Callback done!");
        //        // grid.dataBind(result.results);
        //        // grid.dataBind(result);
        //    }
        //});
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

    function pressEnter($row) {
        scope.onEdit();
    }

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.AD_Roles/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort
                })
                .done()
                .then(function (res) {
                    _.each(res.items, function (val) { val.user_group = 1; })
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
    //("===============END TABLE==================")
});