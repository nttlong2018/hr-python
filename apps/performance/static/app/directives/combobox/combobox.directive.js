(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('inputCombobox', combobox);

    combobox.$inject = ['templateService'];
    
    function combobox(templateService) {
        // Usage:
        //     <input-combobox></input-combobox>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            scope: {
                listCode: "@",
                listValue: "=",
                currentItem: "="
            },
            templateUrl: templateService.getTemplatePath('combobox')
        };
        return directive;

        function link(scope, element, attrs) {
            if (attrs.hasOwnProperty("required")) {
                $(element).wrap("<span zb-required></span>")
            }
            var btn = element.find('button');
            scope.api_url = templateService.getApiCombobox();
            scope.combobox_info = null;
            scope.removeItem = removeItem;
            scope.item = null;//Single select

            getData(function () { assignDataInit(); });

            btn.click(function () {
                //getData(function () {
                    openDialog(scope.combobox_info.display_name, "directives/combobox/template", function () {
                        setTimeout(function () {
                            $(window).trigger('resize');
                        }, 200)
                    }, "myComboboxDialog");
                //});
            });

            /**
            * Hàm mở dialog
            * @param {string} title Tittle của dialog
            * @param {string} path Đường dẫn file template
            * @param {function} callback Xử lí sau khi gọi dialog
            * @param {string} id Id của form dialog, default = 'myModal'
            */
            function openDialog(title, path, callback, id = "myComboboxDialog") {
                //check tồn tại của form dialog theo id
                if ($('#' + id).length === 0) {
                    scope.headerTitle = title;
                    //Đặt ID cho form dialog
                    dialog(scope, id).url(path).done(function () {
                        callback();
                        //Set draggable cho form dialog
                        $('#' + id).ready(function () {
                            $('#' + id + ' .modal-dialog .modal-content .modal-header').on('mousedown touchstart', function (e) {
                                $('#' + id + ' .modal-dialog').draggable();
                            }).bind('mouseup touchend', function () {
                                $('#' + id + ' .modal-dialog').draggable('destroy');
                            });
                        })
                    });
                }
            }

            /**
             * Hàm get data combobox
             */
            function getData(callback) {
                 /*
                 *      Response data
                 *{
                 *  "data" : [], //Datasource
                 *  "display_name" : "", //Title dialog
                 *  "display_fields" : [], //Cột table
                 *  "value_field" : "", //Cột values được chọc khi check
                 *  "caption_field" : "", //Cột name được hiển thị khi check
                 *  "sorting_field" : [], //Trình tự sort data
                 *  "filter_field" : [], //Cột được where khi search
                 *  "error": "" //Lỗi trả về
                }*/
                services.api(scope.api_url)
                    .data({
                        //parameter at here
                        "key": scope.listCode,
                        "value": scope.listValue,
                        "code": scope.currentItem
                    })
                    .done()
                    .then(function (res) {
                        scope.combobox_info = res;
                        scope.combobox_info.data;
                        if(scope.currentItem)
                            assignDataInit();
                        scope.$applyAsync();

                        if (!scope.combobox_info.error)
                            callback();
                    })
            }

            function assignDataInit() {
                var prop = {};
                prop[scope.combobox_info.value_field] = scope.currentItem;

                var obj = _.findWhere(scope.combobox_info.data.items, prop);
                if (obj) {
                    scope.item = {
                        "value": obj[scope.combobox_info.value_field],
                        "caption": obj[scope.combobox_info.caption_field]
                    }
                    scope.$applyAsync();
                }
            }

            function removeItem() {
                scope.currentItem = null;
                scope.item = null;
                scope.$applyAsync();
            }

            scope.$watch('item', function (val) {
                if (val) {
                    scope.currentItem = val['value'];
                    scope.$applyAsync();
                }
            });

            scope.$watch('currentItem', function (newVal, oldVal) {
                if (newVal != oldVal) {
                    assignDataInit();
                }
            })

        }

    }

})();