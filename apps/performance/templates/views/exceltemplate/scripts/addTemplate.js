(function (scope) {
    //Table danh sách người dùng - START
    scope.tableListUserFields = [
        { "data": "field_name", "title": "${ get_res('field_name_table_header', 'Tên trường') }" },
        { "data": "header_text", "title": "${ get_res('header_text_table_header', 'Mô tả') }" },
        { "data": "lookup_data", "title": "${ get_res('lookup_data_table_header', 'Dữ liệu tra cứu') }" },
        { "data": "lookup_key_field", "title": "${ get_res('lookup_key_field_table_header', 'Khóa tra cứu') }" },
        { "data": "lookup_result", "title": "${ get_res('lookup_result_table_header', 'Kết quả tra cứu') }" },
        { "data": "is_visible", "title": "${ get_res('is_visible_table_header', 'Hiển thị') }" },
        { "data": "is_key", "title": "${ get_res('is_key_table_header', 'Khóa chính') }" },
        { "data": "allow_null", "title": "${ get_res('allow_null_table_header', 'Không được để trống') }" },
    ];
    scope.title = scope.$parent.headerTitle;
    scope.tableListUserSource = _loadDataListUserServerSide;
    scope.refreshDataListUserRow = function () { /*Do nothing*/ };
    scope.selectedListUserItems = [];
    scope.ListUserCurrentItem = null;
    scope.onSelectTableRow = pressEnter;
    function _loadDataListUserServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$table_List_User_Config = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
        //setTimeout(function () {
        if (fnReloadData) {
            if (searchText) {
                _tableData("${get_api_key('app_main.api.HCSSYS_ExcelTemplate/get_datail_with_searchtext')}", iPage, iPageLength, orderBy, searchText, function (data) {
                    fnReloadData(data);
                    scope.entity.users = data.data;
                });
            } else {
                _tableData("${get_api_key('app_main.api.HCSSYS_ExcelTemplate/get_datail_with_searchtext')}", iPage, iPageLength, orderBy, null, function (data) {
                    fnReloadData(data);
                });
            }
        }
        //}, 1000);
    };

    function pressEnter($row) {

    }

    /**
    * Hàm load data cho table
    * @param {string} url
    * @param {number} iPage
    * @param {number} iPageLength
    * @param {any} orderBy
    * @param {string} searchText
    * @param {void} callback
    */
    function _tableData(url, iPage, iPageLength, orderBy, searchText, callback) {
        if (scope.__mode == 2) {
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api(url)
                    .data({
                        //parameter at here
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "sort": sort,
                        "where": {
                            "function_id": scope.entity.function_id
                        }
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
    }

    //Hàm load data table - END
    scope._tableData = _tableData;

    scope.onResizeDialog = onResizeDialog;
    scope.__mode = scope.$parent.mode;

    scope.entity = scope.__mode != 1 ? scope.$parent.currentItem : null;
    if (scope.__mode === 2 && scope.entity.users === []) {
        scope.entity.users = [];
    }
    scope.cbbDataDomain = [];

    scope.check = check;

    scope.addDetail = addDetail;

    //Scope select vùng dữ liệu
    scope.selectedItems = [];

    scope.$applyAsync();

    function onResizeDialog() {
        $('.modal-dialog').toggleClass('resize-width');
        //scope.col = scope.col == 4 ? 6 : 4;
        setTimeout(function () {
            $(window).trigger('resize');
        }, 100);
    }

    function check(event) { };

    function saveNNext() {
        if (scope.entity != null) {
            var rsCheck = checkError();//Kết quả check input
            if (rsCheck.result) {
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            beforeCallToServer();
            editData(scope.entity, function (res) {
                if (res.error == null) {
                    if (scope.__mode == 1 || scope.__mode == 3) {
                        //Reload table data
                        reloadData();
                    } else if (scope.__mode == 2) {
                        var entity = JSON.parse(JSON.stringify(scope.entity));
                        scope.$parent.currentItem = entity;
                        afterCallToServer();
                        scope.$applyAsync();
                        scope.$parent.$apply();
                        //Refesh datatable
                        scope.$parent.refreshDataRow();
                    }
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                    scope.entity = null;
                    scope.__mode = 1;
                } else {
                    if (res.error.code == 'duplicate') {
                        var msg = '';
                        _.each(res.error.fields, function (val) {
                            if (val == "role_code")
                                msg += "${get_res('role_code','Mã nhóm người dùng')}" + " " + "${get_global_res('exists','đã tồn tại')}" + "\n";
                            if (val == "role_name")
                                msg += "${get_res('role_name','Tên nhóm người dùng')}" + " " + "${get_global_res('exists','đã tồn tại')}" + "\n";
                            if (val == "dd_code")
                                msg += "${get_res('dd_code','Vùng dữ liệu truy cập')}" + " " + "${get_global_res('exists','đã tồn tại')}" + "\n";
                        });
                        $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", msg, function () { });
                    }
                }
            });
        }
    };

    function addDetail() {
        debugger
        openDialog("${ get_res('reference_information', 'Thông tin tra cứu') }", "exceltemplate/form/addDetail", function () { }, "addDetailTemplate");
    }

    function deleteUser() {
        if (!scope.selectedListUserItems || scope.selectedListUserItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.auth_user/remove_role_code_by_user')}")
                    .data({
                        "users": scope.selectedListUserItems
                    })
                    .done()
                    .then(function (res) {
                        if (res.error == null) {
                            _tableData("${get_api_key('app_main.api.auth_user/get_list_with_searchtext')}", scope.$$table_List_User_Config.iPage,
                                scope.$$table_List_User_Config.iPageLength, scope.$$table_List_User_Config.orderBy,
                                scope.$$table_List_User_Config.SearchText, scope.$$table_List_User_Config.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.selectedListUserItems = null;
                            scope.ListUserCurrentItem = [];
                        } else {
                            $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                        }
                    })
            });
        }
    }

    /**
    * Hàm mở dialog
    * @param {string} title Tittle của dialog
    * @param {string} path Đường dẫn file template
    * @param {function} callback Xử lí sau khi gọi dialog
    * @param {string} id Id của form dialog, default = 'myModal'
    */
    function openDialog(title, path, callback, id = "myModal") {
        //check tồn tại của form dialog theo id
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }

    function editData(param, callback) {
        var url = getUrl();
        var parameter = JSON.parse(JSON.stringify(param));
        if (scope.__mode == 3) {
            //Loại bỏ các propery của angular ra khỏi object
            delete currentItem.$$regKey;
            delete currentItem._id;
            delete currentItem.$$selectKey;
        }
        services.api(url)
            .data(parameter)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    /**
     * Function check input
     */
    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        //Check role_code
        valid = lv.Validate(scope.entity.role_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === false ? "" : "${get_res('error_role_code_null_or_whitespace','Mã nhóm người dùng không được để trống')}" + "\n";
        if (rs.result === true)
            return rs;
        //Check role_name
        valid = lv.Validate(scope.entity.role_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === false ? "" : "${get_res('error_role_name_null_or_whitespace','Tên nhóm người dùng không được để trống')}" + "\n";
        if (rs.result === true)
            return rs;
        //dd_code
        valid = lv.Validate(scope.entity.dd_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === false ? "" : "${get_res('error_dd_code_null_or_whitespace','Vùng dữ liệu truy cập không được để trống')}" + "\n";
        if (rs.result === true)
            return rs

        return rs;
    }

    function reloadData() {
        var tableConfig = scope.$parent.$$tableConfig;
        scope.$parent._tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }

    function beforeCallToServer() {
        if (!scope.entity.hasOwnProperty("stop") || !scope.entity.stop)
            scope.entity.stop = false;
        scope.$applyAsync();
    }

    function afterCallToServer() {
        scope.entity = null;
    }

    function getUrl() {
        return scope.__mode == 1 || scope.__mode == 3 ? "${get_api_key('app_main.api.AD_Roles/insert')}" /*Mode 1: Tạo mới*/
            : "${get_api_key('app_main.api.AD_Roles/update')}" /*Mode 2: Cập nhật*/
    }

    function __init__() { };

});