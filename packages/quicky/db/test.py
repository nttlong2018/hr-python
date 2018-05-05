import expr
import database
import datetime

import datetime
qr=database.connect(host="localhost",
           name="hrm",
           port=27017,
           user="",
           password="123456")

qr=qr.collection("test_from_long").aggregate()

# qr.project(
#     dict(
#         FullName="toUpper(concat(FirstName,' ',LastName))",
#         Age="year(@time_now)- year(BirthDate)",
#         Username=1,
#         CreatedOn=1
#     ),
#     time_now=datetime.datetime.now()
# )
qr.match("12>12",time_now="")


print  qr._pipe


print qr.get_list()
# ret=qr.entity().insert_one(dict(
#     username="a01",
#     password="test"
# ))
# x=expr.parse_expression_to_json_expression("Login.Name>2")
# ret=qr.where("username=='A01'").pull(x).commit()
# # x=expr.get_tree("(Login[{0}].Test.Name>2)and(Username.Name=='x')",1,2)
# print ret
# qr=qr.where("a==1 and b=={0}","X")
# qr=qr.where_and("c==1")
# ret=qr.get_list()
# print item


