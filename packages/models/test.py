import sys
sys.path.append("E:\\code\\python\\p2018\\packages")
import hrm
from excel import exporter
hrm.connect(
    host="localhost",
    port=27017,
    name="hrm",
    user="root",
    password="123456"
)
emp=hrm.employees()
# ret=emp.update(
#                dict(
#                Code="emp2",
#                Username="001"),
#                 "Code=='emp1'")


# lst=emp.delete("Code==@code",code="nv001")
#     .aggregate()
# emp.sort(
#     Code=1,
#     Name=-1
# )
# lst=emp.get_page(
#     page_size=50,
#     page_index=0
# )
data=emp.get_list()
file="E:\\code\\python\\p2018\\packages\\excel\\test.xlsx"
# exporter.write_to(file,data,[
#     dict(
#         field="Code",
#         type="string"
#     ),
#     dict(
#         field="FirstName",
#         type="string"
#     ),
#     dict(
#             field="LastName",
#             type="string"
#          )
# ])
ret=exporter.read_from_file(file)
for item in ret["data"]:
    emp.insert(item)
print("xong")

