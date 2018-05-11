from django.contrib.auth.models import User
import sys
import os
sys.path.append("/home/hcsadmin/argo/packages")
import hrm
from excel import exporter
hrm.connect(
    host="172.16.7.63",
    port=27017,
    name="lv01_lms",
    user="sys",
    password="123456"
)
emp=hrm.employees()
deps=hrm.departments()
position=hrm.positions()
provinces=hrm.provinces()

data=emp.get_list()
def get_data_file(file):
    return os.getcwd()+os.sep+"packages/models/data"+os.sep+file

# file="E:\\code\\python\\p2018\\packages\\excel\\test.xlsx"
# file_cv="E:\\code\\python\\p2018\\packages\\excel\\cv.xlsx"
# file_bp="E:\\code\\python\\p2018\\packages\\excel\\bp.xlsx"
# file_province="E:\\code\\python\\p2018\\packages\\excel\\province.xlsx"

ret=exporter.read_from_file(get_data_file("employees.xlsx"))

coll=hrm.employees()
coll=coll.aggregate()
# coll.project(
#     monthly_salaray="(OfficialInfo.BasicSalary/26)*30",
#     salaray="OfficialInfo.BasicSalary"
# )
# coll.project(
#     monthly_salaray=1,
#     salaray=1,
#     IsOK="iif(monthly_salaray>salaray,1,0)",
#     Rank="switch(case(salaray/26<200000,'Thap'),'Khong biet')",
#     day_salary="ifNull(salaray/26,0)"
#
# )
# coll.group(
#     _id=dict(
#         name="a"
#     ),
#     selectors=dict(
#         full_name="sum(strLenCP(concat(FirstName,' ',LastName)))"
#     )
# )
# lst=coll.get_list()
for item in ret["data"]:
    try:
        user = User.objects.create_user(item["Code"],
                                        item.get("email", item["Code"]+"@gmail.com"),
                                        "123")
        user.first_name = item["FirstName"]
        user.last_name = item["LastName"]
        user.save()
    except:
        print("error")

    # coll.save(item,ret["keys"])
print("xong")

