(function() {
    'use strict';

    angular.module('ZebraApp.components.tables')
        .directive('tableData', ["$parse", tableData]);

    /** @ngInject */
    function tableData($parse) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: true,
            templateUrl: "../performance/static/app/components/table/table-data/table-data.html",
            link: function($scope, elem, attr) {
                var _config = {
                    dataSource: attr["source"],
                    fields: attr["fields"],
                    type: attr["type"], //None,SingleSelect,MultiSelect(checkbox)
                    paging: (attr["paging"] && attr["paging"].toLowerCase() == "false") ? false : true, //fefault:true
                    pageLength: (attr["pageLength"]) ? parseInt(attr["pageLength"]) : 30, //default: 30,
                    serverSide: (attr["serverSide"] && attr["serverSide"].toLowerCase() == "true") ? true : false, //default:false 
                    pressEnter: attr["pressEnter"],
                    selectedItems: attr["selectedItems"],
                    currentItem: attr["currentItem"],
                    searchText: attr["searchText"]
                }
                var $isFirstTime = true;
                var _tableTypes = {
                    None: "None",
                    SingleSelect: "SingleSelect",
                    MultiSelect: "MultiSelect"
                };
                var _dataInput = [];

                if (!_config.dataSource || !_config.fields) {
                    return;
                }

                $scope.currentItem = {};

                function _fnSetCurrentItem($data) {
                    $scope.currentItem = $data;
                    $parse(_config.currentItem).assign($scope.$parent, $data);
                    $scope.$applyAsync();
                }
                // ("Danh sách các fields lấy dữ liệu và tiêu đề cho mỗi field")
                //var tableFields = _config.fields.split(" ").join("").split(",");
                var tableFields = $scope.$eval(_config.fields);

                $scope.tableFields = [], $scope.tableCaptions = [];
                for (var prop in tableFields) {
                    $scope.tableFields.push(prop);
                    $scope.tableCaptions.push(tableFields[prop]);
                }
                var tableData = $scope.$eval(_config.dataSource);
                $scope.tableRecords = [];


                $.each(tableData, function(i, row) {
                    var rowData = [];
                    $.each($scope.tableFields, function(idx, field) {
                        rowData.push(row[field]);
                    })

                    row["$$resKey"] = "object:" + i
                    rowData.data = row;

                    _dataInput.push(row)
                    $scope.tableRecords.push(rowData);
                });
                $scope.$applyAsync();


                //("Sự kiện chọn một cell trên table")
                $scope.$selectCell = function(record, $event) {
                    if ($event.isTrigger) {
                        _fnSetCurrentItem(record.data);
                    }
                }


                $scope.selectedData = [];
                //("Sự kiện chọn một row khi check vào checkbox")
                $scope.$selectCheck = function(record, $event) {
                    var checkbox = $($event.target);
                    //Chặn ko để sự kiện focus của trình duyệt khi nhấn chuột
                    checkbox.blur();

                    function _createSelectedData(data, isSelected) {
                        if (isSelected) {
                            var notExists = _.filter($scope.selectedData, function(f) {
                                return f["$$resKey"] == data["$$resKey"];
                            }).length == 0;
                            if (notExists) {
                                $scope.selectedData.push(data);
                            }
                        } else {
                            $scope.selectedData = _.filter($scope.selectedData, function(f) {
                                return f["$$resKey"] != data["$$resKey"];
                            });
                        }
                        $parse(_config.selectedItems).assign($scope.$parent, $scope.selectedData);
                        $scope.$applyAsync();
                    }

                    if ($event.isTrigger) {
                        _createSelectedData(record.data, checkbox.parent().hasClass("selected"));
                    } else {
                        setTimeout(function() {
                            _createSelectedData(record.data, checkbox.parent().hasClass("selected"));
                        }, 30);
                    }
                }

                // ("Chỉ hiện thanh phân trang nếu số record lớn hơn số giới hạn của 1 trang hoặc có sử dụng phân trang từ server")
                _config.paging = (((tableData.length > _config.pageLength) || _config.serverSide) && _config.paging) ? true : false;

                var dataTableConfigs = {
                    searching: true,
                    lengthChange: false,
                    paging: _config.paging,
                    //"paging":   false,
                    "ordering": true,
                    //bPaginate: false,
                    pageLength: _config.pageLength,
                    pagingType: "numbers",
                    displayStart: 0,

                    // "fnDrawCallback": function(oSettings) {
                    //     alert('DataTables has redrawn the table');
                    // },

                    //"bFilter": false,
                    "info": false,
                    //"bAutoWidth": false,
                    keys: true,


                    // serverSide: true,
                    // ajax: function(data, callback, settings) {
                    //     var dataSource = [] //getDataTable();

                    //     ("Nếu có sử dụng checkbox, giới hạn dữ liệu đủ trên trang")
                    //     for (var i = 0; i < dataSource.length; i++) {
                    //         dataSource[i].unshift('');
                    //     }

                    //     // for (var i = data.start, ien = data.start + data.length; i < ien; i++) {
                    //     //     out.push([i + '-1', i + '-2', i + '-3', i + '-4', i + '-5']);
                    //     // }

                    //     setTimeout(function() {
                    //         callback({
                    //             draw: data.draw,
                    //             data: dataSource.slice(0, data.length),
                    //             recordsTotal: 500,
                    //             recordsFiltered: 500
                    //         });
                    //     }, 50);
                    // },

                    // scrollY: "300px",
                    // scrollX: true,
                    // scrollCollapse: true,
                    // paging: true,
                    // fixedColumns: {
                    //     leftColumns: 1,
                    //     rightColumns: 1
                    // },

                    //fixedHeader: true,
                    //colReorder: true,
                    order: [
                        [1, 'asc']
                    ],
                };
                if (_config.type == _tableTypes.MultiSelect) {
                    dataTableConfigs.columnDefs = [{
                        orderable: false,
                        className: 'select-checkbox',
                        targets: 0
                    }];
                    dataTableConfigs.select = {
                        style: 'multi', //os, single
                        selector: 'td:first-child'
                    };
                } else if (_config.type == _tableTypes.SingleSelect) {
                    dataTableConfigs.select = true;
                } else {
                    dataTableConfigs.select = false;
                }

                setTimeout(function() {
                    var table = $(elem).DataTable(dataTableConfigs);
                    if (_config.type == _tableTypes.MultiSelect) {
                        table.on("click", "th.select-checkbox", function() {
                            if ($("th.select-checkbox").hasClass("selected")) {
                                table.rows().deselect();
                                $scope.selectedData = [];
                                $(elem.find("th.select-checkbox")).removeClass("selected");
                            } else {
                                table.rows().select();
                                $scope.selectedData = _dataInput;
                                $(elem.find("th.select-checkbox")).addClass("selected");
                            }
                            $parse(_config.selectedItems).assign($scope.$parent, $scope.selectedData);
                            $scope.$applyAsync();
                        }).on("select deselect", function() {
                            //("Some selection or deselection going on")
                            if (table.rows({
                                    selected: true
                                }).count() !== table.rows().count()) {
                                $("th.select-checkbox").removeClass("selected");
                            } else {
                                $("th.select-checkbox").addClass("selected");
                            }
                        });
                    }
                    table.on('page.dt', function() {
                            // ("Sự kiện khi chọn button phân trang")
                            $(elem).find("tr.zb-table-row-focus").removeClass("zb-table-row-focus");
                            _fnSetCurrentItem({});
                            var info = table.page.info();
                        })
                        .on('key', function(e, datatable, key, cell, originalEvent) {
                            //("Chạy khi nhấn enter vào checkbox")
                            var rowFocus = cell.row(cell.index().row);
                            if (key == 13) {
                                if (_config.type == _tableTypes.MultiSelect) {
                                    if ($(cell.node()).hasClass("select-checkbox")) {
                                        if ($(rowFocus.node()).hasClass("selected")) {
                                            rowFocus.deselect();
                                        } else {
                                            rowFocus.select();
                                        }
                                        angular.element(cell.node()).triggerHandler('click');
                                    }
                                } else if (_config.type == _tableTypes.SingleSelect) {
                                    rowFocus.select();
                                    angular.element(cell.node()).triggerHandler('click');
                                }
                                if (_config.type != _tableTypes.None) {
                                    var fnPressEnter = $scope.$eval(_config.pressEnter);
                                    if (!$(cell.node()).hasClass("select-checkbox")) {
                                        if (angular.isFunction(fnPressEnter)) {
                                            fnPressEnter($scope.currentItem);
                                        }
                                    }
                                }
                            }
                        })
                        .on('key-focus', function(e, datatable, cell) {
                            var currRow = $(cell.node()).closest("tr");
                            var tbl = $(cell.node()).closest("table");
                            tbl.find("tr.zb-table-row-focus").removeClass("zb-table-row-focus");
                            currRow.addClass("zb-table-row-focus");

                            if (!$(cell.node()).hasClass("select-checkbox")) {
                                angular.element(cell.node()).triggerHandler('click');
                            }
                        })
                        .on('order.dt', function() {
                            //("Sự kiện sắp xếp trên table")
                            $(elem).find("tr.zb-table-row-focus").removeClass("zb-table-row-focus");
                            _fnSetCurrentItem({});
                            var order = table.order();
                        });
                    // .on('key-blur', function(e, datatable, cell) {
                    //     //events.prepend('<div>Cell blur: <i>' + cell.data() + '</i></div>');
                    // })
                    // $('#next').on('click', function() {
                    //     alert("next");
                    //     table.page('next').draw('page');
                    // });

                    // $('#previous').on('click', function() {
                    //     alert("previous")
                    //     table.page('previous').draw('page');
                    // });

                    $scope.$parent.$watch(_config.searchText, function(val, oVal) {
                        if (!$isFirstTime) {
                            //("Search trên toàn bộ bảng")
                            $(elem).find("tr.zb-table-row-focus").removeClass("zb-table-row-focus");
                            _fnSetCurrentItem({});
                            table.search(val).draw();

                            //("Search theo field cố định")
                            // $('input', this.footer()).on('keyup change', function() {
                            //     if (that.search() !== this.value) {
                            //         that
                            //             .search(this.value)
                            //             .draw();
                            //     }
                            // });
                        }
                    })
                }, 10);
            }
        };
    }
})();