# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime

def get_list(args):
    items = models.HCSSYS_Departments().aggregate().project(
        department_code = 1,
        department_name = 1,
        parent_code = 1
        )
    
    return items.get_list()