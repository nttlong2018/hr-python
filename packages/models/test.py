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
hrm.employees().insert_one(
    code="NV001",
    first_name=""

)