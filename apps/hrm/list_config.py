# -*- coding: utf-8 -*-
_lits_config_cache={}
def regist_lits(name,config):
    global _lits_config_cache
    if not _lits_config_cache.has_key(name):
        _lits_config_cache.update({
            name:config
        })
def get_columns(name):
    global _lits_config_cache
    return _lits_config_cache[name].get("columns",[])
basic_cloumns=[
    dict(
        caption="Mã",
        field="Code"
    ),
    dict(
        caption="Tên",
        field="Name"
    ),
    dict(
        caption="Ghi chú",
        field="Description"
    )
]
def extend_columns(cols,ext_cols):
    ret=[]
    ret.extend(cols)
    ret.extend(ext_cols)
    return  ret