# -*- coding: utf-8 -*-
import threading

global lock
lock=threading.Lock()
_caching={}


def get_form_col(fields,index):
    if index % 2==0:
        field_name=fields[index/2]["name"]
        return {
            "is_label":True,
            "caption":fields[index/2]["caption"]
        }
    else:
        return {
            "is_label":False,
            "field":fields[(index-1) / 2]["name"],
            "type":fields[(index-1) / 2].get("type","text")
        }
def create(app_name,layout_name):
    global _caching
    if not _caching.has_key(app_name):
        _caching.update({
            app_name:{}
        })
    if not _caching[app_name].has_key(layout_name):
        _caching[app_name].update({
            layout_name:{}
        })
    return view(_caching[app_name],layout_name)
def extend_columns(cols,ext_cols):
    ret=[]
    ret.extend(cols)
    ret.extend(ext_cols)


    return  ret
class view():
    _data={}
    _layout_name=""
    def __init__(self,data,_layout_name):
        self._data=data
        self._layout_name=_layout_name
        self._data.update({
            _layout_name: {}
        })
    def create(self,config):
        self._data[self._layout_name]=config
        return self
    def get_table_columns(self):
        ret = self._data[self._layout_name].get("columns", [])
        ret = sorted(ret, key=lambda item: item.get("display_index", 0))
        ret = [x for x in ret if x.get("display_in_table", True)]
        return ret
    def get_form(self):
        return self._data[self._layout_name]["form"]
    def find_caption(self,field_name):
        cols = self._data[self._layout_name].get("columns", [])
        ret=[x for x in cols if x.get("name", "")==field_name]
        if ret.__len__()>0:
            return ret[0].get("caption",field_name)
        else:
            return field_name

    def get_form_col(self,fields,index):

        if index % 2 == 0:
            field_name = fields[index / 2]["name"]
            caption=self.find_caption(field_name)
            return {
                "is_label": True,
                "caption": fields[index / 2].get("caption",caption)
            }
        else:
            return {
                "is_label": False,
                "field": fields[(index - 1) / 2]["name"],
                "type": fields[(index - 1) / 2].get("type", "text"),
                "source":fields[(index - 1) / 2].get("source", ""),
                "lookup_field": fields[(index - 1) / 2].get("lookup_field", ""),
                "display_field": fields[(index - 1) / 2].get("display_field", ""),
            }
    def get_config(self):
        return self._data[self._layout_name]
    def get_all_fields_of_form(self):
        ret={}
        form=self.get_form()
        for row in form["rows"]:
            for field in row["fields"]:
                if not ret.has_key(field["name"]):
                    ret.update({
                        field["name"]: 1
                    })

        return ret


