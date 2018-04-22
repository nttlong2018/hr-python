# # -*- coding: utf-8 -*-
# _list_config_cache={}
# def regist_list(name,config):
#     global _list_config_cache
#     if not _list_config_cache.has_key(name):
#         _list_config_cache.update({
#             name:config
#         })
# def get_columns(name):
#     global _list_config_cache
#     return _list_config_cache[name].get("columns",[])
# basic_cloumns=[
#     dict(
#         caption="Mã",
#         field="Code",
#         display_index=100,
#         display_in_table=True,
#         display_in_form=True
#     ),
#     dict(
#         caption="Tên",
#         field="Name",
#         display_index=200,
#         display_in_table=True,
#         display_in_form=True
#     ),
#     dict(
#         caption="Ghi chú",
#         field="Description",
#         display_index=300,
#         display_in_table=True,
#         display_in_form=True
#     )
# ]
# def extend_columns(cols,ext_cols):
#     ret=[]
#     ret.extend(cols)
#     ret.extend(ext_cols)
#
#
#     return  ret
# def get_config(name):
#     global _list_config_cache
#     return _list_config_cache.get(name,{})
# def get_table_columns(name):
#     global _list_config_cache
#     ret=_list_config_cache[name].get("columns",[])
#     ret = sorted(ret, key=lambda item: item.get("display_index", 0))
#     ret=[x for x in ret if x.get("display_in_table",True)]
#     return ret
# def get_form(name):
#     global _list_config_cache
#     return _list_config_cache[name]["form"]