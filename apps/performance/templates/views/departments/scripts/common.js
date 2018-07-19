(function (scope) {
    scope.entity = null;
    scope.onSave = onSave;
    //scope.__mode = scope.$parent.__mode;
    scope.__mode = 1;


    function onSave() {
        $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_res('Notify_Save','Bạn có muốn lưu không?')}", function () {
            var url = scope.__mode === 1 ? "${get_api_key('app_main.api.HCSSYS_Departments/insert')}" 
            : "${get_api_key('app_main.api.HCSSYS_Departments/update')}" ;
            callApi(url, scope.entity, function (res) {
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                } else if (res.error.hasOwnProperty('code') && res.error.code == "duplicate") {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${ get_res('department_code', 'Mã phòng ban') }" + "${get_global_res('exists','đã tồn tại')}", function () { });
                } else if (res.error.hasOwnProperty('code') && res.error.code == "missing") {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('missing_fields','Nhập liệu thiếu')}" + "\n" + 
                        "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                } else {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                }
            })
        });
    }

    /**
     * Hàm gọi api
     * @param {string} url
     * @param {object} parameter
     * @param {void} callback
     */
    function callApi(url, parameter, callback) {
        console.log(parameter)
        services.api(url)
            .data(parameter)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    scope.$watch('entity', function(val){
        console.log(val);
    })
});