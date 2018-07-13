import database
qr=query.connect(host="localhost",
           name="hrm",
           port=27017,
           user="",
           password="123456")
hr_emp=qr.collection("hrm.employees")
hr_department=qr.collection("hrm.departments")
# hr_emp.insert_one(
#     EmployeeCode="NV0021",
#     FirstName="Nicle",
#     LastName="Kanga"
# ).commit()
# item=hr_emp.where("EmployeeCode=='nv001'").update(dict(
#     DepartmentCode="BPKT"
# )).commit()
# hr_department.insert_one(
#     DepartmentCode="BPKT",
#     DepartmentName="Phong Ke Toan"
# ).commit()
# hr_emp.aggregate().lookup(source=hr_department,
#                           local_field="DepartmentCode",
#                           foreign_field="DepartmentCode",
#                           alias="Dep")\
#     .unwind("Dep")

lst=hr_emp.aggregate().get_list()
print lst