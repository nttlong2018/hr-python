var _ws_url_
var _wsOnBeforeCall;
var _wsOnAfterCall;
function ws_set_url(url){
    _ws_url_=url;
}
function ws_onBeforeCall(callback){
    _wsOnBeforeCall=callback
}
function ws_onAfterCall(callback){
    _wsOnAfterCall=callback
}
function ws_get_url(){
    return _ws_url_;
}
function ws_call(api_path,view_path,data,cb){
    return new Promise(function(resolve,reject){
        sender=undefined;
        if(_wsOnBeforeCall){
            sender=_wsOnBeforeCall()
        }
          $.ajax({
            url: ws_get_url(),
            type: "post",
            dataType: "json",
            data: JSON.stringify({
                   path:api_path,
                   view:view_path,
                   data:data
            }) ,
            success: function (res) {
                if(_wsOnAfterCall){
                    _wsOnAfterCall(sender)
                }
               if(cb){
                cb(undefined,res)
               }
               else{
                resolve(res)
               }

            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(_wsOnAfterCall){
                    _wsOnAfterCall(sender)
                }
                var newWindow = window.open();
                newWindow.document.write(errorThrown);
                if(cb){
                    cb({
                        error:{
                            type:"server"
                        }
                    })
                }
                else {
                reject({
                        error:{
                            type:"server"
                        }
                    })}

            }


        });

    })

}
function ws(scope){
    function ret(scope){
        var me=this;

        me.api=function(_api){
            function ret_api(_api){
                var _me=this;
                _me._api=_api;
                _me.data=function(_data){
                    _me._data=_data;
                    return _me;
                }
                _me.done=function(cb){
                       if(!scope.view_path){
                            throw("view_path is empty")
                       }
                       return ws_call(_me._api,scope.view_path,_me._data,cb)

                }
            }

            return new ret_api(_api);
        }


    }
    return new ret(scope)
}
