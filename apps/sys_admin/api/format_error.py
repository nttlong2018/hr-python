def html_format(fields,request,view,reason):
    ret_fields=[{"caption": request.get_app_res("{0}.data-field.{1}".format(view, x), x), "name": x} for x in fields]
    html_msg="<ul>"
    for item in ret_fields:
        html_msg+="<li>"+item["caption"]+"</li>"
    html_msg+="</ul>"
    msg_reason=""
    if reason=="missing":
        msg_reason=request.get_app_res("miss_require_field_error","Please, enter below fields")
    elif reason=="duplicate":
        msg_reason = request.get_app_res("duplicate_field_error",
                                         "The value of below fields is ready to use, please select another value:")
    else:
        raise (Exception("'reason' must be 'missing' or 'duplicate'"))

    ret_html="<legend><fieldset>{0}</fieldset>{1}</legend>".format(msg_reason,html_msg)
    return dict(

        fields=ret_fields,
        msg=ret_html

    )