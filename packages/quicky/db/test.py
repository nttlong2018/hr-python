import expr
import query
import datetime
# qr=query.get_query(
#
# )
# # x=expr.get_tree("(employee_code=={0} and "
#                 "employee_name=={2} and "
#                 "department=='001') or "
#                 "contains(name,{2})",
#                     "test cai coi","a","b")
# y=expr.get_expr(x,"a","b","c")
import datetime
qr=query.connect(host="localhost",
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
qr.match("contains(username,@time_now)",time_now="").unwind("$users")

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


