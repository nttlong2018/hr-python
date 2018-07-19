(function (scope) {
    //("===============BEGIN TABLE==================")
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "dd_code", "title": "Mã vùng dữ liệu", "format": "uppercase" },
        { "data": "dd_name", "title": "Tên vùng vùng dữ liệu", "format": "lowercase" },
        { "data": "description", "title": "Mô tả chi tiết"},
        { "data": "display_access_mode", "title": "Phạm vi truy cập" },
        { "data": "created_on", "title": "Thời điểm tạo", "format": "date:dd/MM/yyyy" }
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
    scope._tableData = _tableData;
    scope.mapAccess_mode = [];
    scope.getDisplayNameAccessMode = getDisplayNameAccessMode;

    /**
     * Hàm mở form chỉnh sửa
     */
    function onEdit() {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog('Chỉnh sửa vùng truy cập', '../pages/permission/form/addDomain', function () { });
        } else {
            $msg.message('Thông báo', 'Không có dòng được chọn', function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog('Thêm mới vùng truy cập', '../pages/permission/form/addDomain', function () { });
    }

    function onDelete() {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message('Thông báo', 'Không có dòng được chọn', function () { });
        } else {
            $msg.confirm('Thông báo', 'Bạn có muốn xóa không?', function () {
                services.api("${get_api_key('app_main.api.HCSSYS_DataDomain/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert('Thao tác thành công', $type_alert.SUCCESS);
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
            openDialog('Thêm mới vùng truy cập', '../pages/permission/form/addDomain', function () { });
        } else {
            $msg.message('Thông báo', 'Không có dòng được chọn', function () { });
        }
    }

    function onSearch(val) {
        scope.tableSearchText = scope.SearchText;
        scope.$apply();
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
     * @param {function} callback Xử lí sau khi gọi dialog\
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        //check tồn tại của form dialog theo id
        if ($('#myModal').length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id).url(path).done(function () {
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
    console.log("CUrrent Scope", scope);
    function pressEnter($row) {
        scope.onEdit();
    }

    function getDisplayNameAccessMode(code) {
        var name = '';
        _.each(scope.mapAccess_mode, function (val) {
            if (val.value == code) {
                name = val.caption;
                return;
            }
        })
        return name;
    }

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
                    _.each(res.items, function (val) {
                        val.display_access_mode = getDisplayNameAccessMode(val.access_mode);
                    });
                    callback(data);
                    //scope.tableSource = res;
                    scope.currentItem = null;
                    scope.$apply();
                })
    }

    function _comboboxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                //parameter at here
                "language": "VN",
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