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
deps=hrm.departments()
position=hrm.positions()

data=emp.get_list()
file="E:\\code\\python\\p2018\\packages\\excel\\test.xlsx"
file_cv="E:\\code\\python\\p2018\\packages\\excel\\cv.xlsx"
file_bp="E:\\code\\python\\p2018\\packages\\excel\\bp.xlsx"

ret=exporter.read_from_file(file_bp)
# for item in ret["data"]:
#     data_item=emp.find_one("Code==@code",code=item["Code"])
#     if data_item!=None:
#         emp.update(item,"Code==@code",code=item["Code"])
#     else:
#         emp.insert(item)
# for item in ret["data"]:
#     data_item=position.find_one("Code==@code",code=item["Code"])
#     if data_item!=None:
#         position.update(item,"Code==@code",code=item["code"])
#     else:
#         position.insert(item)
for item in ret["data"]:
    data_item=deps.find_one("Code==@code",code=item["Code"])
    if data_item!=None:
        deps.update(item,"Code==@code",code=item["Code"])
    else:
        deps.insert(item)

print("xong")

