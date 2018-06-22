window.set_component_template_url('${get_static("app/directives/")}')
angular
    .module("admin", ["c-ui", 'ZebraApp.components', 'hcs-template'])
    .factory("systemService", service)
    .controller("admin", controller);

controller.$inject = ["$dialog", "$scope", "systemService"];
dialog_root_url('${get_app_url("pages/")}')
function controller($dialog, $scope, systemService) {
    $scope.$root.systemConfig = null;/*HCSSYS_SystemConfig*/
    $scope.$root.language = "${get_language()}";
    $scope.VIEW_ID = "${register_view()}"
    $dialog($scope)
    ws_set_url("${get_app_url('api')}")
    ws_set_export_token_url("${get_api_key('app_main.excel.manager/generate_token')}");
    ws_onBeforeCall(function () {
        mask = $("<div class='mask'></div>")
        mask.appendTo("body");
        return mask
    });
    ws_onAfterCall(function (mask) {
        mask.remove();
    })
    history_navigator($scope.$root);
    
    $scope.view_path = "${get_view_path()}";
    $scope.services = services = ws($scope);
    $scope.$root.system = systemService;
    $scope.$root.collapseSubMenu = function collapseSubMenu(e, id) {
        e.stopPropagation();
        $('#hcs-top-bar-menu ul li ul').slideUp();
        if (id != '' && ($('#' + id).css('display') != 'block')) {
            $('#' + id).slideDown(500);
        }
    };

    //Đồng hồ
    $scope.$root.timer = {
        clock: Clock(),
        meridiem: getMeridiem(),
        date: Calendar()
    };
    setInterval(function () {
        $scope.$root.timer.clock = Clock();
        if ($scope.$root.timer.clock === "00:00") {
            $scope.$root.timer.date = Calendar();
            $scope.$root.timer.meridiem = getMeridiem();
        }
        $scope.$root.$applyAsync();
    }, 10000);

    /**
     * Initialize Data
     */
    function activate() {
        $scope.$root.currentFunction = '';
        $scope.$root.currentModule = '';
        $scope.$root.logo = 'http://surehcs.lacviet.vn/WS2017/Customers/default/logo.png';

        //Get function list
        services.api("${get_api_key('app_main.api.functionlist/get_list')}")
            .data({
                //parameter at here
            })
            .done()
            .then(function (res) {
                var functions = JSON.parse(JSON.stringify(res));
                /**
                 * Customize string tittle group when display data
                 */
                $.each(res, function (idx, val) {
                    if (val.parent_id == null) {
                        var arr = val["custom_name"].split("/");
                        var display_name = arr[0];
                        var display_name_bold = arr[1];
                        val["display_name"] = display_name;
                        val['display_name_bold'] = display_name_bold;
                    }
                });

                var fs = _.filter(res, function (d) {
                    return d["parent_id"] == null;
                });
                $.each(fs, function (idx, val) {
                    val["child_items"] = _.filter(res, function (d) {
                        return d["parent_id"] == val["function_id"];
                    });
                });
                $scope.$root.$functions = fs;
                $scope.$applyAsync();
                $scope.$root.getPage = function () {
                    if (angular.isDefined($scope.$root.page)) return "${get_app_url('')}/pages/" + $scope.$root.page
                    return "${get_app_url('')}/pages/home"
                }
                $scope.$root.$history.change(function (data) {
                    console.log("$history.change app.js", data);
                    if (data.hasOwnProperty("")) {
                        set_function_id(HOMEPAGE_ID);
                    }
                    if (data.page) {
                        var currentFunction = _.filter(functions, function (d) {
                            return d["url"] == data.page;
                        });
                        if (currentFunction.length > 0) {
                            $scope.$root.currentFunction = currentFunction[0].custom_name.replace("/", " ");
                            set_function_id(currentFunction[0].function_id);
                            $scope.$root.currentModule = _.filter(functions, function (d) {
                                return d["function_id"] == currentFunction[0].parent_id;
                            })[0].custom_name.replace("/", " ");
                        } else {
                            set_function_id(HOMEPAGE_ID);
                        }
                    } else {
                        $scope.$root.currentFunction = $scope.$root.currentModule = null;
                        set_function_id(HOMEPAGE_ID);
                    }
                    $scope.$root.page = data.page;
                    $scope.$root.page_data = data;
                    $scope.$root.$applyAsync();
                })
            })

        //Get HCSSYS_SystemConfig
        services.api("${get_api_key('app_main.api.common/get_config')}")
            .data({
                //parameter at here
            })
            .done()
            .then(function (res) {
                //Set HCSSYS_SystemConfig
                $scope.$root.systemConfig = res;
            })
    }
    /**
     * Init
     */
    activate();
}

function service() {
    var fac = {};
    var currentRow;

    fac.guid = function() {
        function s4(){
                return Math.floor((1 + Math.random()) * 0x10000)
                    .toString(16)
                    .substring(1);
            }
            return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
    };

    return fac;
};

function Clock() {
    return moment().locale("${get_language()}").format("HH:mm");
}

function toStartCase(str) {
    return str
        .toLowerCase()
        .split(' ')
        .map(function (word) {
            return word[0].toUpperCase() + word.substr(1);
        })
        .join(' ');
}

function Calendar() {
    return toStartCase(moment().locale("${get_language()}").format('dddd, DD MMMM, YYYY'));
}

function getMeridiem() {
    return moment().locale("${get_language()}").format("a");
}