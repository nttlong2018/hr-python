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
provinces=hrm.provinces()

data=emp.get_list()
file="E:\\code\\python\\p2018\\packages\\excel\\test.xlsx"
file_cv="E:\\code\\python\\p2018\\packages\\excel\\cv.xlsx"
file_bp="E:\\code\\python\\p2018\\packages\\excel\\bp.xlsx"
file_province="E:\\code\\python\\p2018\\packages\\excel\\province.xlsx"

ret=exporter.read_from_file(file_province)
coll=emp

for item in ret["data"]:
    coll.save(item,ret["keys"])
print("xong")

