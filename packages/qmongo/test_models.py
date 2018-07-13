# -*- coding: utf-8 -*-
# from helpers import validators
import helpers
import database
from helpers import get_model
from qview import create_mongodb_view
helpers.define_model(
    "base",
    [["Code"]],
    dict(
        Code=helpers.create_field("b"),
        F=helpers.create_field("X",False)
    )
)

def on_before_insert(data):

    data["ParentCode"]=None
    data["Paths"]=[1]
helpers.events("base").on_before_insert(on_before_insert)

helpers.extent_model(
    "departments",
    "base",
    [],
    dict(

        PanretCode=helpers.create_field("text"),
        Paths=helpers.create_field("list",True,"text")
    )
)


db=database.connect(
    host="172.16.7.63",
    port=27017,
    user="test",
    password="test",
    name="test"
)
# ret=db.collection("departments").insert(
#     Code="A01"
# )
ret=db.collection("departments")
ret.switch_schema("long_test")
x=ret.aggregate()
v=create_mongodb_view(x,"test_cai_coi")
items=v.get_list()
print items
# ret=ret.update({
#     "Code":"C1"
# },"paths=={0}","a01")
# print(ret)
