(function (scope) {
    scope.entity = null;
    scope.cbbDateFormat = null;
    scope.cbbDecPlaceSeparator = null;
    scope.cbbDefaultLanguage = null;
    scope.onSave = onSave;
    scope.$parent.$parent.$parent.onSave = scope.onSave;

    /**
     * Event Nhấn save
     */
    function onSave() {
        $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_res('Notify_Save','Hệ thống sẽ cần khởi động lại để áp dụng thay đỗi này.')}", function () {
            callApi("${get_api_key('app_main.api.HCSSYS_SystemConfig/update')}", scope.entity, function (res) {
                if (res.error == null) {
                    //Set lại HCSSYS_SystemConfig sau khi chỉnh sửa
                    var config = JSON.parse(JSON.stringify(scope.entity));
                    scope.$root.systemConfig = config;
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                } else {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                }
            })
        });
    }

    /**
     * Get data combobox
     */
    function _comboboxData() {
        var $url = "${get_api_key('app_main.api.SYS_ValueList/get_list')}";
        callApi($url, { "name": "LDateFormat" }, function (res) {
            scope.cbbDateFormat = res.values;
            scope.$applyAsync();
        })

        callApi($url, { "name": "LDefaultLanguage" }, function (res) {
            scope.cbbDefaultLanguage = res.values;
            scope.$applyAsync();
        })

        callApi($url, { "name": "LDecPlaceSeparator" }, function (res) {
            console.log(res);
            scope.cbbDecPlaceSeparator = res.values;
            scope.$applyAsync();
        })
    }

    /**
     * Hàm gọi api
     * @param {string} url
     * @param {object} parameter
     * @param {void} callback
     */
    function callApi(url, parameter, callback) {
        services.api(url)
            .data(parameter)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    /**
     * Initialize
     */
    function __init__() {
        var config = JSON.parse(JSON.stringify(scope.$root.systemConfig));
        scope.entity = config;
        scope.$applyAsync();
        //Init combobox data
        _comboboxData();
    }

    __init__();
});