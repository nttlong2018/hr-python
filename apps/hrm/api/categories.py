import quicky
import hrm.forms as forms
from qmongo import helpers
from qmongo import database
import hash_data
from bson import *
app=quicky.applications.get_app_by_file(__file__)
db=database.connect(app.settings.Database)
def get_list(params):
    frm=getattr(forms,params["data"]["path"])
    if frm==None:
        raise Exception("form was not found")
    coll_name=frm.layout.get_config()["collection"]
    coll=db.collection(coll_name).aggregate()
    project={}
    lookup_cols=frm.layout.get_lookups()
    for item in lookup_cols:
        coll.lookup(
            source=item["source"],
            local_field=item["local_field"],
            foreign_field=item["foreign_field"],
            alias=item["alias"]
        )
        coll.unwind(item["alias"])




    for item in frm.layout.get_table_columns():
        project.update({
            item["name"]:1
        })
    count=coll.copy()
    count.count("totalItems")
    total_items =count.get_item()
    if total_items==None:
        total_items=0
    else:
        total_items=total_items["totalItems"]

    coll.project(project)
    items= coll.get_list()
    return dict(
        items=items,
        totalItems=total_items,
        pageIndex=0,
        pageSize=20
    )
def get_item(params):
    category_name=params["view"].split('/')[1]
    frm = getattr(forms, category_name)
    coll_name = frm.layout.get_config()["collection"]
    data=params["data"]

    coll = db.collection(coll_name).aggregate()
    project = {}
    select_fields=frm.layout.get_all_fields_of_form()
    ret_item=coll.project(frm.layout.get_all_fields_of_form()).match("_id==@id",id=ObjectId(data["_id"])).get_item()
    return ret_item
def save_item(params):
    category_name = params["view"].split('/')[1]
    frm = getattr(forms, category_name)
    coll_name = frm.layout.get_config()["collection"]
    data = params["data"]
    coll = db.collection(coll_name)
    if data.get("_id",None)==None:
        coll.insert(data)
    else:
        update_fields=frm.layout.get_all_fields_of_form()
        update_data={}
        for key in update_fields:
            if data.has_key(key) and key not in frm.layout.get_config().get("keys",[]):
                update_data.update({
                    key:data[key]
                })
        coll.update(update_data,"_id==@id",id=ObjectId(data["_id"]))
    return data
def get_dictionary(params):
    category_name = params["view"].split('/')[1]
    frm = getattr(forms, category_name)
    data =params["data"]
    source_id=params["data"]["source"]
    source=hash_data.from_hash(source_id)

    frm = getattr(forms, category_name)
    lookup=frm.layout.get_lookup_config_by_source(source)
    ret_data=db.collection(lookup["source"]).aggregate().project(
        _id="0",
        value=lookup["lookup_field"],
        text=lookup["display_field"]
    ).get_list()
    return ret_data



