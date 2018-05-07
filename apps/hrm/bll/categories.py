from hrm import list_config
from hrm.bll import db
from hrm import forms
import datetime
from bson.objectid import ObjectId
import quicky

app=quicky.applications.get_app_by_file(__file__)
cnn=quicky.mongodb.connect(app.settings.DATABASE)
def get_list(data):
    form_name = data["view"].split("/")[1]
    form = getattr(forms, form_name)

    coll = db.coll(form.layout.get_config()["collection"])
    project={}
    for col in form.layout.get_table_columns():
        project.update({
            col["name"]:1
        })
    ret_items=list(
        coll.aggregate([
            {
                "$project":project
            }
        ])
    )
    return dict(
        items=ret_items,
        page_index=0,
        page_size=50,
        total_items=ret_items.__len__()
    )
def add_item(data):
    form_name=data["view"].split("/")[1]
    form=getattr(forms,form_name)
    insert_data=data.get("data",{})
    insert_data.update({
        "CreatedOn":datetime.datetime.now(),
        "CreatedOnUTC":datetime.datetime.utcnow(),
        "CreatedBy":data["user"].username

    })

    ret=db.coll(form.layout.get_config()["collection"]).insert_one(insert_data)
    insert_data.update({
        "_id":ret.inserted_id
    })
    print (ret)
    return insert_data
def get_item(data):
    form_name = data["view"].split("/")[1]
    form = getattr(forms, form_name)
    selector=form.layout.get_all_fields_of_form()
    ret_data=list(db.coll(form.layout.get_config()["collection"])
    .aggregate([
        {
            "$match":{
                "_id":ObjectId(data["data"]["id"])
            }
        },
        {
            "$project":selector
        }
    ]))
    if ret_data.__len__()==0:
        return {}
    else:
        return ret_data[0]
def update_item(data):
    form_name = data["view"].split("/")[1]
    form = getattr(forms, form_name)
    updater={}
    for key in data["data"].keys():
        if key!="_id" and key[0:1]!="$":
            updater.update({
                key:data["data"][key]
            })
    updater.update({
        "ModifedOn":datetime.datetime.now(),
        "ModifedOnUtc":datetime.datetime.utcnow(),
        "ModifiedBy":data["user"].username
    })
    db.coll(form.layout.get_config()["collection"]).update_one({
        "_id":ObjectId(data["data"]["_id"])
    },{
        "$set":updater
    })
    return updater



    # selector = form.layout.get_all_fields_of_form()
    # ret_data = list(db.coll(form.layout.get_config()["collection"])
    #     .aggregate([
    #     {
    #         "$match": {
    #             "_id": ObjectId(data["data"]["id"])
    #         }
    #     },
    #     {
    #         "$project": selector
    #     }
    # ]))
    # if ret_data.__len__() == 0:
    #     return {}
    # else:
    #     return ret_data[0]
def get_data_source(data):
    ret=cnn.collection(data["data"]["source"])\
        .aggregate()\
        .project(
        value=data["data"]["lookup-field"],
        text=data["data"]["display-field"])\
        .get_list()
    return ret



