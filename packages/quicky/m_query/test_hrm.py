import query
qr=query.get_query(host="localhot",
           name="hrm",
           port=27017,
           user="",
           password="123456")
hr_emp=qr.collection("hrm.employees")
hr_emp.find_one()