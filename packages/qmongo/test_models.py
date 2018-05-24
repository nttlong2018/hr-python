# -*- coding: utf-8 -*-
# from helpers import validators
import helpers
import database
from helpers import get_model
# validators.create_model("test",
#                         {
#                             "Code":"text",
#                             "Name":"text",
#                             "Gender":"bool",
#                             "WorkingInfo.DepartmentCode":"text",
#                             "WorkingInfo.LoginList":"list"
#
#                         })
# ret=validators.validate_type_of_data("test",{
#     "WorkingInfo":{
#         "DepartmentCode":"tffghj",
#         "LoginList":[
#             {
#                 "LoginTime":"dasda"
#             }
#         ]
#
#     }
#
# })
# print(ret)
# helpers.define_model(
#     "test",
#     ["Code","WorkingInfo.DepartmentCode"],
#     {
#         "Code":helpers.create_field("text",True),
#         "Name":helpers.create_field("text",True),
#         "WorkingInfo":{
#             "DepartmentCode":helpers.create_field("text",True),
#             "JoinDate":helpers.create_field("date",True)
#         }
#     }
# )
helpers.define_model(
    "Employees",
    ["Code"],
    Code=helpers.create_field("text",True),
    Name=helpers.create_field("text",True),
    WorkingInfo=dict(
        DepartmentCode=helpers.create_field("text",True),
        JoinDate=helpers.create_field("date",True)
    )
)
helpers.define_model(
    "sys_users",
    [],
    Username=helpers.create_field("text",True),
    NickName=helpers.create_field("text",True)

)
helpers.define_model(
    "test",
    [],
    A=helpers.create_field("text"),
    B=helpers.create_field("text")
)

# import helpers
# helpers.define_model(
#     "Employees",
#     ["Code"],
#     {
#         "Code":helpers.create_field("text",True),
#         "Name":helpers.create_field("text",True),
#         "WorkingInfo.DepartmentCode":helpers.create_field("text",True),
#         "WorkingInfo.JoinDate":helpers.create_field("date",True)
#     }
# )
import datetime
# ret=validators.validate_require_data("test",{
#         "Code":"NV001",
#         "Name":"Test",
#         "WorkingInfo.JoinDate":datetime.datetime.now(),
#         "WorkingInfo.DepartmentCode":"BP001"
#     })
# ret2=validators.validate_type_of_data("test",{
#     "Code":False
# })
db=database.connect(
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    name="lv01_lms"
)
#
ret=db.collection("sys_users").aggregate().project(

    name="(concat(Username,'',NickName))",
).project(
    full_name="name+'A'"
)
ret.lookup(
    source="test",
    local_field="full_name",
    foreign_field="A",
    alias="X"
    ).unwind("X").project(
    m=1
).match("m>2")
ret.sort(
    m=1
)
# model=get_model("Employees")
# ret=model.validate_expression("(concat(firstname,'',lastname)+workingInfo.code.fx)=={0}",None,["c"])
lst=ret.get_list()
print(lst)
# print(ret2)