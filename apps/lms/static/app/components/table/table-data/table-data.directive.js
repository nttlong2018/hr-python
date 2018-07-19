(function() {
    'use strict';

    angular.module('ZebraApp.components.tables')
        .directive('tableData', ["$parse", "$filter", tableData]);

    /** @ngInject */
    function tableData($parse, $filter) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                dataSource: "=source", //"Database của table"
                fields: "=", //"Danh sách các fields lấy dữ liệu và tiêu đề cho mỗi field"
                type: "@", //None,SingleSelect,MultiSelect(checkbox)
                pageLength: "=", //default: 30,
                paging: "=", //default:true
                serverSide: "=", //default:false 
                pressEnter: "=",
                selectedItems: "=",
                currentItem: "=",
                searchText: "=",
                refreshRow: "=",
                responsive: "=",
                languageResource: "="
            },
            //template: '<table class="display zb-data-table responsive nowrap"></table>',
            templateUrl: "../performance/static/app/components/table/table-data/table-data.html",
            link: function($scope, elem, attr) {
                var table = null;

                function _initLayout() {
                    $scope.pageLength = ($scope.pageLength) ? $scope.pageLength : 30;

                    if (table) {
                        table.destroy();
                        //Xóa toàn bộ events đã gắn trc
                        table.off("click")
                            .off("select deselect")
                            .off("page.dt")
                            .off("key")
                            .off("key-focus")
                            .off("order.dt");
                        $(elem).empty();
                        table = null;
                    }
                    var _tableTypes = {
                        None: "None",
                        SingleSelect: "SingleSelect",
                        MultiSelect: "MultiSelect"
                    };

                    // if (!$scope.dataSource || !$scope.dataSource) {
                    //     return;
                    // }

                    var _curentRowIndex = -1;
                    //setdata cho item hiện đang được chọn
                    function _fnSetCurrentItem($data) {
                        $scope.currentItem = $data;
                        $scope.$applyAsync();
                    }
                    var _selectedItems = [];
                    //set data cho danh sách row được chọn
                    function _fnSetSelectedItems($item, $isSelected) {
                        if ($isSelected) {
                            var notExists = _.filter(_selectedItems, function(f) {
                                return f["$$regKey"] === $item["$$regKey"];
                            }).length === 0;
                            if (notExists) {
                                _selectedItems.push($item);
                            }
                        } else {
                            _selectedItems = _.filter(_selectedItems, function(f) {
                                return f["$$regKey"] !== $item["$$regKey"];
                            });
                        }
                        $scope.selectedItems = _selectedItems;
                        //$parse(_config.selectedItems).assign($scope.$parent, _selectedItems);
                        $scope.$applyAsync();
                    }

                    if ($scope.type === _tableTypes.MultiSelect) {
                        if (!$scope.serverSide) {
                            $.each($scope.dataSource, function(i, v) {
                                v["$$selectKey"] = null;
                                v["$$regKey"] = i;
                            });
                        }

                        var _isExistsSelectedKey = _.filter($scope.fields, function(f) {
                            return f["data"] === "$$selectKey"
                        }).length > 0;
                        if (!_isExistsSelectedKey) {
                            $scope.fields.unshift({ "data": "$$selectKey", "targets": 0 });
                        }
                    }

                    //format columns
                    $.each($scope.fields, function(i, v){
                        if(v.format){
                            var $s = v.format.split(":");
                            if($s[0].toLowerCase() === 'date'){
                                //Add function render to columns
                                //$filter('date')(date, format, timezone)
                                v.render = function(data, type, row) {
                                    let $r;
                                    switch($s.length){
                                        case 3:
                                            $r =  $filter('date')(data, $s[1], $s[2]);
                                            break;
                                        case 2:
                                            $r =  $filter('date')(data, $s[1]);
                                            break;
                                        default:
                                            $r =  $filter('date')(data);
                                    }
                                    return $r;
                                }
                            } else if($s[0].toLowerCase() === 'number'){
                                //Add function render to columns
                                //$filter('number')(number, fractionSize)
                                v.render = function(data, type, row) {
                                    let $r;
                                    switch($s.length){
                                        case 2:
                                            $r =  $filter('number')(data, $s[1]);
                                            break;
                                        default:
                                            $r =  $filter('number')(data);
                                    }
                                    return $r;
                                }
                            } else if($s[0].toLowerCase() === 'currency'){
                                //Add function render to columns
                                //$filter('currency')(amount, symbol, fractionSize)
                                v.render = function(data, type, row) {
                                    let $r;
                                    switch($s.length){
                                        case 3:
                                            $r =  $filter('currency')(data, $s[1], $s[2]);
                                            break;
                                        case 2:
                                            $r =  $filter('currency')(data, $s[1]);
                                            break;
                                        default:
                                            $r =  $filter('currency')(data);
                                    }
                                    return $r;
                                }
                            } else if($s[0].toLowerCase() === 'lowercase'){
                                //Add function render to columns
                                //$filter('lowercase')()
                                v.render = function(data, type, row) {
                                    return $filter('lowercase')(data);
                                }
                            } else if($s[0].toLowerCase() === 'uppercase'){
                                //Add function render to columns
                                //$filter('uppercase')()
                                v.render = function(data, type, row) {
                                    return $filter('uppercase')(data);
                                }
                            } else if($s[0].toLowerCase() === 'json'){
                                //Add function render to columns
                                //$filter('json')(object, spacing)
                                v.render = function(data, type, row) {
                                    let $r;
                                    switch($s.length){
                                        case 2:
                                            $r =  $filter('json')(data, $s[1]);
                                            break;
                                        default:
                                            $r =  $filter('json')(data);
                                    }
                                    return $r;
                                }
                            }
                        }
                    });

                    // ("Chỉ hiện thanh phân trang nếu số record lớn hơn số giới hạn của 1 trang hoặc có sử dụng phân trang từ server")
                    var _paging = (($scope.serverSide || ($scope.dataSource && $scope.dataSource.length > $scope.pageLength)) && $scope.paging) ? true : false;
                    var dataTableConfigs = {
                        columns: $scope.fields,
                        searching: true,
                        lengthChange: false,
                        paging: _paging,
                        //"paging":   false,
                        ordering: true,
                        //bPaginate: false,
                        pageLength: $scope.pageLength,
                        pagingType: "numbers",
                        displayStart: 0,

                        // "fnDrawCallback": function(oSettings) {
                        //     alert('DataTables has redrawn the table');
                        // },

                        //"bFilter": false,
                        info: true,
                        "bAutoWidth": true,
                        keys: true,
                        destroy: true,

                        ////search theo từng columns (Search theo field cố định)
                        // initComplete: function() {
                        //     var api = this.api();

                        //     // Apply the search
                        //     api.columns().every(function() {
                        //         var that = this;

                        //         $('input', this.footer()).on('keyup change', function() {
                        //             if (that.search() !== this.value) {
                        //                 that
                        //                     .search(this.value)
                        //                     .draw();
                        //             }
                        //         });
                        //     });
                        // },

                        responsive: false,
                        scrollY: true,
                        scrollX: false,
                        scrollCollapse: false,
                        // fixedColumns: {
                        //     leftColumns: 1,
                        //     //rightColumns: 1
                        // },

                        //fixedHeader: true,
                        //colReorder: true,
                        order: [
                            [1, 'asc']
                        ],
                    };
                    dataTableConfigs.language = ($scope.languageResource) ?
                        $scope.languageResource : {
                            //"sProcessing": "Đang xử lý...",
                            //"sLengthMenu": "Xem _MENU_ dòng",
                            //"sZeroRecords": "Không tìm thấy dòng nào phù hợp",
                            "sInfo": "_START_-_END_/_TOTAL_", //"Hiển thị _START_ đến _END_ trong tổng số _TOTAL_ dòng",
                            "sInfoEmpty": "0/0", //"Đang xem 0 đến 0 trong tổng số 0 dòng",
                            "sInfoFiltered": "| &#931;_MAX_", //"(được lọc từ _MAX_ dòng)",
                            //"sInfoPostFix": "",
                            //"sSearch": "Tìm:",
                            //"sUrl": "",
                            // "oPaginate": {
                            //     "sFirst": "Đầu",
                            //     "sPrevious": "Trước",
                            //     "sNext": "Tiếp",
                            //     "sLast": "Cuối"
                            // },
                            select: {
                                rows: {
                                    _: " | &#9745; %d", //(Đã  chọn %d dòng)", //"%d rows selected"
                                    0: "", //"Click a row to select it ",
                                    1: " | &#9745; 1" //"Đã chọn 1 dòng"
                                }
                            }
                        }
                    if ($scope.responsive) {
                        dataTableConfigs.responsive = true;
                    } else {
                        dataTableConfigs.scrollX = true;
                    }
                    if ($scope.dataSource) {
                        if ($scope.serverSide) {
                            dataTableConfigs.serverSide = true;
                            dataTableConfigs.ajax = _loadDataServerSide;

                            function _loadDataServerSide(data, callback, settings) {
                                //Data source của server side bắt buộc là một function
                                if (angular.isFunction($scope.dataSource)) {
                                    var _initCallback = function(ret) {
                                        $.each(ret.data, function(i, v) {
                                            v["$$selectKey"] = null;
                                            v["$$regKey"] = i;
                                        });
                                        callback(ret);
                                    };
                                    var _sort = [];
                                    if (data.order && data.order.length > 0) {
                                        $.each(data.order, function(i, v) {
                                            _sort.push({
                                                columns: data.columns[v.column].data,
                                                type: v.dir
                                            })
                                        });
                                    }
                                    //Tính số trang hiện tại
                                    var _pageIndex = (data.length > data.start) ? 1 : (Math.ceil(data.start / data.length) + 1);
                                    if (data.search.value && data.search.value.trim()) {
                                        $scope.dataSource(_initCallback, _pageIndex, data.length, _sort, data.search.value);
                                    } else {
                                        $scope.dataSource(_initCallback, _pageIndex, data.length, _sort, null);
                                    }
                                } else {
                                    callback({
                                        "recordsTotal": 0,
                                        "recordsFiltered": 0,
                                        "data": []
                                    })
                                }
                                setTimeout(function() {
                                    var _bindResize = false;
                                    if (!_bindResize) {
                                        $(window).resize(function() {
                                            _bindResize = true;
                                            var _tableWrapper = $(elem).closest("div.dataTables_wrapper");
                                            var _tableScrollBody = $(elem).closest("div.dataTables_scrollBody");

                                            //32: height of paginator and others
                                            var _heightTableWrapperParent = _tableWrapper.parent().height();
                                            var _heightOuterTable = Math.round(_tableWrapper.height() - _tableScrollBody.height() + 32);
                                            _tableScrollBody.css({
                                                "height": (Math.round(_heightTableWrapperParent - _heightOuterTable)) + "px"
                                            });
                                        });
                                    }
                                    $(window).trigger("resize");
                                }, 300);
                            };
                        } else {
                            dataTableConfigs.data = $scope.dataSource;
                        }
                    }

                    if ($scope.type === _tableTypes.MultiSelect) {
                        dataTableConfigs.columnDefs = [{
                            orderable: false,
                            className: 'select-checkbox',
                            targets: 0
                        }];
                        dataTableConfigs.select = {
                            style: 'multi', //os, single
                            selector: 'td:first-child'
                        };
                    } else if ($scope.type === _tableTypes.SingleSelect) {
                        dataTableConfigs.select = true;
                    } else {
                        dataTableConfigs.select = false;
                    }
                    //setTimeout(function() {
                    table = $(elem).DataTable(dataTableConfigs);
                    var _tableWrapper = $(elem).closest("div.dataTables_wrapper");
                    var _tableScrollBody = $(elem).closest("div.dataTables_scrollBody");
                    if (!$scope.serverSide) {
                        setTimeout(function() {
                            $(window).trigger("resize");
                        }, 300);
                    }

                    if ($scope.type === _tableTypes.MultiSelect) {
                        function _addEventCheckAll() {
                            var _th_checkAll = $(_tableWrapper.find("table.zb-data-table")[0]).find("th.select-checkbox")
                            _th_checkAll.unbind("click");
                            _th_checkAll.bind("click", function() {
                                if ($(this).hasClass("selected")) {
                                    table.rows().deselect();
                                    _selectedItems = [];
                                    $(this).removeClass("selected");
                                } else {
                                    table.rows().select();
                                    $(this).addClass("selected");

                                    _selectedItems = [];
                                    $.each(table.data(), function(i, v) {
                                        _selectedItems.push(v);
                                    });
                                }
                                $scope.selectedItems = _selectedItems;
                                $scope.$applyAsync();
                            });
                        };
                        _addEventCheckAll();
                        // table.on("click", "th.select-checkbox", function() {
                        //     if ($("th.select-checkbox").hasClass("selected")) {
                        //         table.rows().deselect();
                        //         _selectedItems = [];
                        //         $(elem.find("th.select-checkbox")).removeClass("selected");
                        //     } else {
                        //         table.rows().select();
                        //         _selectedItems = $scope.dataSource;
                        //         $(elem.find("th.select-checkbox")).addClass("selected");
                        //     }
                        //     $scope.selectedItems = _selectedItems;
                        //     //$parse(_config.selectedItems).assign($scope.$parent, _selectedItems);
                        //     $scope.$applyAsync();
                        // });
                        table.on("select deselect", function(e, row) {
                            if (row.node) {
                                _fnSetSelectedItems($scope.currentItem, $(row.node()).hasClass("selected"));
                                //("Some selection or deselection going on")
                                if (table.rows({ selected: true }).count() !== table.rows().count()) {
                                    $(_tableWrapper).find("th.select-checkbox").removeClass("selected");
                                } else {
                                    $(_tableWrapper).find("th.select-checkbox").addClass("selected");
                                }
                            }
                        });
                    }
                    table.on('page.dt', function() {
                            // ("Sự kiện khi chọn button phân trang")
                            $(elem).find("tr.zb-table-row-focus").removeClass("zb-table-row-focus");
                            _curentRowIndex = -1;
                            _fnSetCurrentItem({});
                            if ($scope.serverSide) {
                                $(_tableWrapper).find("th.select-checkbox").removeClass("selected");
                                _selectedItems = [];
                                _fnSetSelectedItems({});
                            }
                            //var info = table.page.info();
                        })
                        .on('key', function(e, datatable, key, cell, originalEvent) {
                            //("Chạy khi nhấn enter vào checkbox")
                            var rowFocus = cell.row(cell.index().row);
                            // _fnSetCurrentItem(cell.row(cell.index().row).data());
                            if (key === 13) {
                                if ($scope.type === _tableTypes.MultiSelect) {
                                    if ($(cell.node()).hasClass("select-checkbox")) {
                                        var $isSelected = $(rowFocus.node()).hasClass("selected");
                                        if ($isSelected) {
                                            rowFocus.deselect();
                                        } else {
                                            rowFocus.select();
                                        }
                                        //Nếu đang đc chọn thì sẽ bỏ chọn và ngược lại
                                        _fnSetSelectedItems($scope.currentItem, !$isSelected);
                                        //angular.element(cell.node()).triggerHandler('click');
                                    }
                                } else if ($scope.type === _tableTypes.SingleSelect) {
                                    rowFocus.select();
                                    //angular.element(cell.node()).triggerHandler('click');
                                }
                                if ($scope.type !== _tableTypes.None) {

                                    if (!$(cell.node()).hasClass("select-checkbox")) {
                                        if (angular.isFunction($scope.pressEnter)) {
                                            $scope.pressEnter(JSON.parse(JSON.stringify($scope.currentItem)));
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
                            _curentRowIndex = cell.index().row;

                            _fnSetCurrentItem(cell.row(cell.index().row).data());
                            // if (!$(cell.node()).hasClass("select-checkbox")) {
                            //     _fnSetCurrentItem(cell.row(cell.index().row).data());
                            // }
                        })
                        .on('order.dt', function() {
                            //("Sự kiện sắp xếp trên table")
                            $(elem).find("tr.zb-table-row-focus").removeClass("zb-table-row-focus");
                            _curentRowIndex = -1;
                            _fnSetCurrentItem({});
                            var order = table.order();
                        });
                    // .on('key-blur', function(e, datatable, cell) {
                    //     //events.prepend('<div>Cell blur: <i>' + cell.data() + '</i></div>');
                    // })
                    // $('#next').on('click', function() {
                    //     table.page('next').draw('page');
                    // });

                    // $('#previous').on('click', function() {
                    //     table.page('previous').draw('page');
                    // });

                    $scope.refreshRow = function() {
                        if (_curentRowIndex > -1) {
                            //var rowData = table.row(_curentRowIndex).data(x);
                            table.row(_curentRowIndex).data($scope.currentItem).invalidate()
                        }
                    }

                    var existsWatchSearch = false;
                    if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                        existsWatchSearch = _.filter($scope.$$watchers, function(f) {
                            return f.exp === "searchText"
                        }).length > 0;
                    }
                    if (!existsWatchSearch) {
                        $scope.$watch("searchText", function(val, old) {
                            //("Search trên toàn bộ bảng")
                            $(elem).find("tr.zb-table-row-focus").removeClass("zb-table-row-focus");
                            _curentRowIndex = -1;
                            _fnSetCurrentItem({});
                            if (val !== old) {
                                table.search(val).draw();
                            }
                        });
                    }

                    var existsWatchDataSource = false;
                    if ($scope.$$watchers && Array.isArray($scope.$$watchers) && !angular.isFunction($scope.dataSource)) {
                        existsWatchDataSource = _.filter($scope.$$watchers, function(f) {
                            return f.exp === "dataSource"
                        }).length > 0;
                    }
                    if (!$scope.serverSide) {
                        if (!existsWatchDataSource) {
                            $scope.$watch("dataSource", function(val, old) {
                                _initLayout();
                            });
                        }
                    }

                }
                _initLayout();

            }
        };
    }
})();