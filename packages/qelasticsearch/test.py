# -*- coding: utf-8 -*-
import openpyxl
import sys
import os
sys.path.append("/home/hcsadmin/argo/packages")
from excel import exporter
import os
import helper
client=helper.connect(
    [
        "http://172.16.7.63:9200"
    ]
)
def get_data_file(file):
    return os.getcwd()+os.sep+"data"+os.sep+file

# file="E:\\code\\python\\p2018\\packages\\excel\\test.xlsx"
# file_cv="E:\\code\\python\\p2018\\packages\\excel\\cv.xlsx"
# file_bp="E:\\code\\python\\p2018\\packages\\excel\\bp.xlsx"
# file_province="E:\\code\\python\\p2018\\packages\\excel\\province.xlsx"

ret=exporter.read_from_file(get_data_file("employees.xlsx"))
index=client.get_all_indexes()
# for item in ret["data"]:
#     client.create("employees_index_1",item,id=item["Code"])
ret_data=client.search_text("employees_index_1","Tuấn")
print(ret_data)
