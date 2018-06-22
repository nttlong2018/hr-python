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
                apiUrl: "@",
                multiSelect: "=",
                selectedItems: "=",
                currentItem: "="
            },
            templateUrl: templateService.getTemplatePath('combobox')
        };
        return directive;

        function link(scope, element, attrs) {
            var btn = element.find('button');
            scope.combobox_info = null;
            scope.removeChoice = removeChoice;
            scope.removeItem = removeItem;
            scope.items = [];//Multi select
            scope.item = null;//Single select

            getData(function () { assignDataInit(); });

            btn.click(function () {
                getData(function () {
                    openDialog(scope.combobox_info.display_name, "directives/combobox/template", function () { }, "myComboboxDialog");
                });
            });

            /**
            * Hàm mở dialog
            * @param {string} title Tittle của dialog
            * @param {string} path Đường dẫn file template
            * @param {function} callback Xử lí sau khi gọi dialog
            * @param {string} id Id của form dialog, default = 'myModal'
            */
            function openDialog(title, path, callback, id = "myComboboxDialog") {
                //if (typeof (id) === 'undefined')
                //    id = "myModal";
                var fn = {
                    "button": [{ "func_name": "saveNClose", "icon": "la la-check", "name": "" }],
                    "close":true
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
                services.api(scope.apiUrl)
                    .data({
                        //parameter at here
                        "key": scope.listCode,
                        "value": scope.listValue
                    })
                    .done()
                    .then(function (res) {
                        scope.combobox_info = res;
                        scope.combobox_info.data;
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

            function getCaptionFromValue(value) {
                var caption = "";
                _.each(scope.selectedItems, function (val) {
                    if (val[scope.combobox_info["value_field"]] == val)
                        caption = val[scope.combobox_info["caption_field"]];
                })
                return caption;
            }

            function removeChoice(value) {
                scope.items = _.without(scope.items, _.findWhere(scope.items, {
                    "value":value
                }));
                scope.selectedItems = removeValue(scope.selectedItems, value);
            }

            function removeValue (array, id) {
                return _.reject(array, function (item) {
                    return item === id; // or some complex logic
                });
            };

            function removeItem() {
                scope.currentItem = null;
                scope.item = null;
                scope.$applyAsync();
            }

            scope.$watch('items', function (val) {
                scope.selectedItems = [];
                _.each(val, function (ele) {
                    scope.selectedItems.push(ele['value']);
                })
                scope.$applyAsync();
            });

            scope.$watch('item', function (val) {
                if (val) {
                    scope.currentItem = val['value'];
                    scope.$applyAsync();
                }
            });

        }

    }

})();