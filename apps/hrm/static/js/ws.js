var _ws_url_
function ws_set_url(url){
    _ws_url_=url;
}
function ws_get_url(){
    return _ws_url_;
}
function ws_call(api_path,view_path,data,cb){
    return new Promise(function(resolve,reject){
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
               if(cb){
                cb(undefined,res)
               }
               else{
                resolve(res)
               }

            },
            error: function(jqXHR, textStatus, errorThrown) {
                if(cb){
                    cb(errorThrown)
                }
                else {
                reject(errorThrown)}

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
