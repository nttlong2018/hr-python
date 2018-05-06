import sys
import os
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
def get_data_file(file):
    return os.getcwd()+os.sep+"data"+os.sep+file

# file="E:\\code\\python\\p2018\\packages\\excel\\test.xlsx"
# file_cv="E:\\code\\python\\p2018\\packages\\excel\\cv.xlsx"
# file_bp="E:\\code\\python\\p2018\\packages\\excel\\bp.xlsx"
# file_province="E:\\code\\python\\p2018\\packages\\excel\\province.xlsx"

ret=exporter.read_from_file(get_data_file("employees.xlsx"))
coll=emp
# coll=coll.aggregate()
# coll.project(
#     monthly_salaray="(OfficialInfo.BasicSalary/26)*30",
#     salaray="OfficialInfo.BasicSalary"
# )
# coll.project(
#     monthly_salaray=1,
#     salaray=1,
#     IsOK="iif(monthly_salaray>salaray,1,0)",
#     Rank="switch(case(salaray/26<200000,'Thap'),'Khong biet')",
#     day_salary="salaray/26"
#
# )
# lst=coll.get_list()
for item in ret["data"]:
    coll.save(item,ret["keys"])
print("xong")

