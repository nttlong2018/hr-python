(function (scope) {
    scope.__mode = 0;
    scope.entity = {};

    scope.$parent.$parent.$parent.onSave = onSave;
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onPrint = onPrint;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;

    function onSave() {
        if (scope.entity != null) {
            var rsCheck = checkError();//Kết quả check input
            if (rsCheck.result) {
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            beforeCallToServer();
            editData(function (res) {
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);//Xuất thông báo thành cônng
                    if (scope.__mode == 1 || scope.__mode == 3) {
                        //Reload table data
                        reloadData();
                    } else if (scope.__mode == 2) {
                        scope.$parent.$parent.$parent.currentItem.full_name = res.entity.last_name + " " + res.entity.first_name;
                        scope.$parent.$parent.$parent.currentItem.gender = res.entity.gender;
                        scope.$parent.$parent.$parent.currentItem.department_name = res.entity.department_name;
                        scope.$parent.$parent.$parent.currentItem.job_w_code = res.entity.job_w_code;
                        scope.$parent.$parent.$parent.currentItem.join_date = res.entity.join_date;
                        //Refesh datatable
                        scope.$parent.$parent.$parent.refreshDataRow();
                        scope.$parent.$parent.$parent.$apply();
                    }
                } else {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                }
            });
        }
    }

    function onAttach() {
        alert('onAttach');
    }

    function onPrint() {
        alert('onAttach');
    }

    function onRefresh() {
        alert('onAttach');
    }

    function editData(callback) {
        var url = getUrl();
        var currentItem = JSON.parse(JSON.stringify(scope.entity));
        services.api(url)
            .data(currentItem)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function beforeCallToServer() {

    }

    function getUrl() {
        return scope.__mode == 1 || scope.__mode == 3 ? "${get_api_key('app_main.api.HCSEM_Employees/insert')}" /*Mode 1: Tạo mới*/
            : "${get_api_key('app_main.api.HCSEM_Employees/update')}" /*Mode 2: Cập nhật*/
    }

    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.employee_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('employee_code_is_not_null','Mã nhân viên không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.last_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('last_name_is_not_null','Họ không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.first_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('first_name_is_not_null','Tên không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.join_date);
        rs.result = valid.isDate();
        rs.errorMsg = rs.result === false ? "${get_res('join_date_is_not_null','Ngày vào làm không được để trống')}" + '\n' : "";
        if (rs.result === false) {
            rs.result = true;
            return rs;
        } else {
            rs.result = false;
        }
        valid = lv.Validate(scope.entity.department_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('department_code_is_not_null','Bộ phậm làm việc không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        //valid = lv.Validate(scope.entity.job_w_code);
        //rs.result = valid.isNullOrWhiteSpace();
        //rs.errorMsg = rs.result === true ? "${get_res('job_w_code_is_not_null','Chức danh không được để trống')}" + '\n' : "";
        //if (rs.result === true) {
        //    return rs;
        //}
        return rs;
    }

    function reloadData() {
        scope.$parent.$parent.$parent.refresh();
    }
    
    function _getEmployee(empCode) {
        if (scope.__mode == 2) {
            services.api("${get_api_key('app_main.api.HCSEM_Employees/get_employee_by_emp_code')}")
                .data({
                    "employee_code": empCode
                })
                .done()
                .then(function (res) {
                    scope.entity = res;
                    scope.$applyAsync();
                })
        }
    }

    $(document).ready(function () {
        $('#email').focusout(function (e) {
            if ($(this).val() != "") { 
                var rs = true;
                var valid = lv.Validate(scope.entity.email);
                rs = valid.isEmail();
                if (rs !== true) {
                    $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", "${get_global_res('email_is_not_valid','Email không hợp lệ')}", function () { });
                    $(this).focus();
                }
            }
        })

        $('#personal_email').focusout(function (e) {
            if ($(this).val() != "") {
                var rs = true;
                var valid = lv.Validate(scope.entity.personal_email);
                rs = valid.isEmail();
                if (rs !== true) {
                    $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", "${get_global_res('personal_email_is_not_valid','Email cá nhân không hợp lệ')}", function () { });
                    $(this).focus();
                }
            }
        })
    })

    function _init_() {
        scope.__mode = scope.$parent.$parent.$parent.mode;
    }

    scope.$parent.$parent.$parent.$watch("mode", function (val) {
        if (val != 0)
            _init_();
    })

    scope.$parent.$parent.$parent.$watchGroup(['mode', 'currentItem'], function (val) {
        if (val[0] != 0) {
            _init_();
            if (val[0] == 2) {
                _getEmployee(val[1].employee_code);
                scope.$applyAsync();
            } else if(val[0] == 1){
                scope.entity = null;
                scope.$applyAsync();
            }
        }
    })
});