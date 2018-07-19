(function (scope) {
    /* Table */
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "template_code", "title": "${get_res('template_code_table_header','Mã template')}" },
        { "data": "template_name", "title": "${get_res('template_name_table_header','Tên template')}" },
        { "data": "view_name", "title": "${get_res('view_name_table_header','Tên bảng')}" },
        { "data": "is_default", "title": "${get_res('is_default_table_header','Là template mặc định')}" }
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

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        if (scope.treeCurrentNode.hasOwnProperty('function_id')) {
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.HCSSYS_ExcelTemplate/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "where": {
                        'function_id':scope.treeCurrentNode.function_id
                    },
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
    }

    scope.onSelectTableRow = pressEnter;
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = function () { /*Do nothing*/ };
    function pressEnter($row) {
        onEdit();
    }

    /* Tree */
    scope.treeCurrentNode = {};
    scope.treeSelectedNodes = [];
    scope.treeSelectedRootNodes = [];
    scope.treeCheckAll = false;
    scope.treeSearchText = '';
    scope.treeDisable = false;
    scope.treeMultiSelect = false;
    scope.treeMode = 1; // Value in (1, 3) combobox toàn quyền set 1 ngược lại set 3
    var _treeDepartmentsDataSource = null;
    //var _treeDefault = null;
    scope.treeDepartmentsDataSource = null;
    scope.mapName = [
        { 'function_id': 'HCSSYS1000', 'name': 'Sơ đồ tổ chức', 'url': 'exceltemplate' },
    ];
    scope.currentFunction = scope.mapName[0];

    /*Event*/
    scope.onAdd = onAdd;
    scope.onEdit = onEdit;
    scope.onCopy = onCopy;
    scope.onDelete = onDelete;
    scope.onSearch = onSearch;
    scope.onImport = onImport;
    scope.onExport = onExport;

    function onEdit() {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('detail_template','Chi tiết template')}", 'exceltemplate/form/addTemplate', function () { }, 'dialogEditTemplate');
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('detail_template','Chi tiết template')}", 'exceltemplate/form/addTemplate', function () { }, 'dialogEditTemplate');
    }

    function onCopy() {

    }

    function onDelete() {

    }

    function onSearch() {

    }

    function onImport() {

    }

    function onExport() {

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
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }

    _functionList();
    function _functionList() {
        services.api("${get_api_key('app_main.api.functionlist/get_tree')}")
            .data()
            .done()
            .then(function (res) {
                console.log("XXXXXXXXXXXXXXXXX", res);
                _treeDepartmentsDataSource = res;
                scope.treeDepartmentsDataSource = _treeDepartmentsDataSource;
                //Tạo biến local dùng để lưu cây trạng thái chưa được chọn
                //_treeDefault = JSON.parse(JSON.stringify(res));
                scope.$applyAsync();
            })
    }

    scope.$root.$history.onChange(scope, function (data) {
        if (scope.mapName.length > 0) {
            if (data.f) {
                scope.$partialpage = _.filter(scope.$root.$functions, function (f) {
                    return f.function_id = data.f
                })[0].url;
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

    scope.$watch('treeCurrentNode', function (val) {
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, scope.$$tableConfig.searchText)
    })
});