import sys
sys.path.append("E:\\code\\python\\p2018\\packages")
import hrm
hrm.connect(
    host="localhost",
    port=27017,
    name="hrm",
    user="root",
    password="123456"
)
emp=hrm.employees().aggregate()
emp.sort(
    Code=1,
    Name=-1
)
lst=emp.get_page(
    page_size=50,
    page_index=0
)
print(lst)
# for x in range(1,1000000):
#     emp.insert(
#         Code="EMP{0}".format(x),
#         FisrtName="Nhan vien 00 {0}".format(x),
#         LastName="test {0}".format(x)
#     )
# hrm.employees().update(
#     dict(
#         FirtsName="Nguyen Van",
#         LastName="Test001"
#     ),
#     "Code=={0}",
#      "nv001"
#
# )
