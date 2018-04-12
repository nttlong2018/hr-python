var _ws_url_
function ws_set_url(url){
    _ws_url_=url;
}
function ws_get_url(){
    return _ws_url_;
}
function ws_call(api_path,data,cb){
    return new Promise(function(resolve,reject){
          $.ajax({
            url: ws_get_url(),
            type: "post",
            dataType: "json",
            data: JSON.stringify({
                   path:api_path,
                   data:data
            }) ,
            success: function (res) {
               if(cb){
                cb(undefine,res)
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
