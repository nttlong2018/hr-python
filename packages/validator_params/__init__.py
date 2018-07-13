def get_value_by_path(path,data):
    items=path.split(".")
    ret=data.get(items[0],None)
    if ret==None:
        return  None
    else:
        for index in range(1,items.__len__()):
            ret=ret.get(items[index],None)
            if ret==None:
                return  None
    return ret

def require(field_list,data):
    ret=[]
    for item in field_list:
        if type(item) in [str,unicode]:
            if get_value_by_path(item,data)==None:
                ret.append(item)
    return ret

