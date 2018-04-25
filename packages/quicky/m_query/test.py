import expr
import query
# qr=query.get_query(
#
# )
# # x=expr.get_tree("(employee_code=={0} and "
#                 "employee_name=={2} and "
#                 "department=='001') or "
#                 "contains(name,{2})",
#                     "test cai coi","a","b")
# y=expr.get_expr(x,"a","b","c")
qr=query.get_query(host="localhost",
           name="hrm",
           port=27017,
           user="",
           password="")
ret=qr.collection("list.provinces").find("Code=='BK'")
print ret


