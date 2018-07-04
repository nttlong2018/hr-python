var lv;
(function (lv) {
    /**
     * Import
     */
    var UploadService = (function () {
        function UploadService() { }
        //function UploadService(controller) {
        //    this.controller = controller;
        //}
        //UploadService.prototype.setProcessMethod = function (path) {
        //    this.processMethod = path;
        //    return this;
        //};
        UploadService.prototype.setContent = function (content) {
            //this._content = content;
            var binary = '';
            var bytes = new Uint8Array(content);
            var len = bytes.byteLength;
            for (var i = 0; i < len; i++) {
                binary += String.fromCharCode(bytes[i]);
            }
            this._content = window.btoa(binary);
            return this;
        };
        UploadService.prototype.setFileName = function (fileName) {
            this._fileName = fileName;
            return this;
        };
        //UploadService.prototype._arrayBufferToBase64 = function (buffer) {
        //    var binary = '';
        //    var bytes = new Uint8Array(buffer);
        //    var len = bytes.byteLength;
        //    for (var i = 0; i < len; i++) {
        //        binary += String.fromCharCode(bytes[i]);
        //    }
        //    return window.btoa(binary);
        //};
        UploadService.prototype.setParams = function (Params) {
            this._params = Params;
            return this;
        };
        UploadService.prototype.afterDone = function (fnAfterDone) {
            this._fnAfterDone = fnAfterDone;
            return this;
        };
        UploadService.prototype.setSize = function (size) {
            this._size = size;
            return this;
        };
        UploadService.prototype.done = function (callback) {
            //this.controller.call("LV.HCS.Uploader/LV.HCS.Uploader.APIs/Upload")
            //    .noMask()
            //    .data({
            //        Path: this.processMethod,
            //        Data: this._arrayBufferToBase64(this._content),
            //        FileName: this._fileName,
            //        Params: JSON.stringify(this._params)
            //    })
            //    .done(function (evt) {
            //        if (callback) {
            //            callback(evt.data);
            //        }
            //    });
            if (callback) {
                callback(this);
            }
        };
        return UploadService;
    }());
    lv.UploadService = UploadService;
    function readFile(callback) {
        var _template = ""
            + "<div class='lv-form-import'>"
            + "     <div class='form-container' style='display: none;'>"
            + "         <div class='form-header'>"
            + "             <span>Import file</span>"
            + "         </div>"
            + "         <div class='form-content'>"
            + "             <input class='import-file' type='file' style='display:none'></input>"
            + "             <span></span>"
            + "             <button class='import-btn-select-file'>Select File</button>"
            + "         </div>"
            + "         <div class='form-footer'>"
            + "             <button class='import-btn-accept'>Accept</button>"
            + "             <button class='import-btn-close'>Close</button>"
            + "         </div>"
            + "     </div>"
            + "</div>"
        var _form = $(_template);
        var _form_container = _form.find(".form-container");
        var _file = _form.find(".import-file");
        var _btnAccept = _form.find(".import-btn-accept");
        var _btnClose = _form.find(".import-btn-close");

        _btnClose.bind("click", function () {
            _form.remove();
        });

        _file.on("change", function (evt) {
            var me = this;
            var inputfile = $(me);
            var file = me.files[0];
            _file.val("");
            //console.log(file);
            var reader = new FileReader();
            reader.onload = function () {
                var arrayBuffer = this.result;
                var array = new Uint8Array(arrayBuffer);
                //var dataparams = {
                //    FunctionID: "sFunctionID",
                //    Customer: "Customer"
                //};
                //if (params) {
                //    $.each(params, function (idx, val) {
                //        dataparams[val.ParamName] = val.ParamValue;
                //    });
                //}
                var _uploadService = new lv.UploadService();
                _uploadService
                    //.setProcessMethod("strApi")
                    .setFileName(file.name)
                    .setContent(array)
                    .setSize(file.size)
                    //.setParams(dataparams)
                    .done(function (res) {
                        _btnAccept.unbind("click");
                        _btnAccept.bind("click", function () {
                            callback(res);
                            _form.remove();
                        });
                    });
            };
            reader.readAsArrayBuffer(file);

        });
        var _btnSelect = _form.find(".import-btn-select-file");
        _btnSelect.bind("click", function () {
            _file.trigger("click");
        });
        _form.appendTo("body");
        _form_container.show("fast");
    }
    var ImportFile = (function () {
        function ImportFile(api) {
            this._api = api;
        }
        //ImportFile.prototype.setLanguage = function (language) {
        //    this._language = language;
        //    return this;
        //};
        //ImportFile.prototype.setFunctionID = function (functionID) {
        //    this._functionID = functionID;
        //    return this;
        //};
        ImportFile.prototype.done = function (callback) {
            var me = this;
            readFile(function (file) {
                var now = new Date();
                var offset_minutes = now.getTimezoneOffset();
                $.ajax({
                    url: ws_get_url(),
                    type: "post",
                    dataType: "json",
                    data: JSON.stringify({
                        path: me._api,
                        view: "view_path",
                        data: file,
                        offset_minutes: offset_minutes
                    }),
                    success: function (res) {
                        if (callback) {
                            callback(res)
                        }
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        var newWindow = window.open();
                        var txt = jqXHR.responseText
                        while (txt.indexOf(String.fromCharCode(10)) > -1) {
                            txt = txt.replace(String.fromCharCode(10), "<br/>")
                        }
                        newWindow.document.write(txt);
                    }
                });
            });
        };
        return ImportFile;
    }());
    lv.ImportFile = function (api) {
        return new ImportFile(api);
    };

    /**
     * Export
     */
    var ExportFile = (function () {
        function ExportFile(path) {
            this._path = path;
        }
        ExportFile.prototype.data = function (data) {
            this._data = data
            return this;
        }
        ExportFile.prototype.done = function () {
            var me = this;
            var now = new Date();
            var offset_minutes = now.getTimezoneOffset();
            $.ajax({
                url: ws_get_url(),
                type: "post",
                dataType: "json",
                data: JSON.stringify({
                    path: ws_get_export_token_url(),
                    view: angular.element(".ng-scope").scope().$root.currentFunction.function_id,
                    data: {
                        path: me._path,
                        function: (angular.element(".ng-scope").scope().$root.currentFunction) ? angular.element(".ng-scope").scope().$root.currentFunction.function_id : HOMEPAGE_ID,
                        params: me._data
                    },
                    offset_minutes: offset_minutes
                }),
                success: function (res) {
                    console.log(res);
                    if (res.link) {
                        window.open(res.link);
                    } else {
                        var newWindow = window.open();
                        newWindow.document.write("<h3>File not found!</h3>");
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    var newWindow = window.open();
                    var txt = jqXHR.responseText
                    while (txt.indexOf(String.fromCharCode(10)) > -1) {
                        txt = txt.replace(String.fromCharCode(10), "<br/>")
                    }
                    newWindow.document.write(txt);
                }
            });
        };
        return ExportFile;
    }());

    lv.ExportFile = function (path) {
        return new ExportFile(path);
    };
})(lv || (lv = {}));
