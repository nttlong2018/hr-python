angular
    .module("admin", ["c-ui", 'ZebraApp.components', 'hcs-template'])
    .factory("systemService", service)
    .controller("admin", controller);

controller.$inject = ["$dialog", "$scope", "systemService"];

function controller($dialog, $scope, systemService) {
    $scope.VIEW_ID = "${register_view()}"
    $dialog($scope)
    ws_set_url("${get_app_url('api')}")
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

    /**
     * Initialize Data
     */
    function activate() {
        $scope.$root.currentFunction = '';
        $scope.$root.currentModule = '';
        $scope.$root.logo = 'http://surehcs.lacviet.vn/WS2017/Customers/default/logo.png';

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
                $scope.$root.$applyAsync();

                $scope.$root.$history.change(function (data) {
                    if (data.page) {
                        var currentFunction = _.filter(functions, function (d) {
                            return d["url"] == data.page;
                        });
                        if (currentFunction.length > 0) {
                            $scope.$root.currentFunction = currentFunction[0].custom_name.replace("/", " ");

                            $scope.$root.currentModule = _.filter(functions, function (d) {
                                return d["function_id"] == currentFunction[0].parent_id;
                            })[0].custom_name.replace("/", " ");
                        }
                    } else {
                        $scope.$root.currentFunction = $scope.$root.currentModule = null;
                    }
                    $scope.$root.page = data.page
                    $scope.$root.$applyAsync();
                })
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