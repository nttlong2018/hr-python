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
emp=hrm.employees()
ret=emp.update(
               dict(
               Code="emp2",
               Username="001"),
                "Code=='emp1'")


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
print(ret)
