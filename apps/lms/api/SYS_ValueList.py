# -*- coding: utf-8 -*-
import models

def get_list(args):
    items = models.SYS_ValueList().aggregate().project(
        language = 1,
        list_name = 1,
        values = 1,
        )

    language = args["data"].get("language", "")
    list_name = args["data"].get("name", "")
    if args["data"].has_key('language') and args["data"].has_key('name'):
        items.match("(language == @lan) and (list_name == @name)", lan=language, name=list_name)
    
    return items.get_item()