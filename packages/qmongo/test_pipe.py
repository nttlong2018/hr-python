from  pymongo import MongoClient

import gridfs
from helpers import filter
from helpers import aggregate
cnn=MongoClient(host="172.16.7.63",port=27017)
db=cnn.get_database("lv01_lms")
db.authenticate("sys","123456")

#
# # fx=filter("a==@test",test='12')
# # fx.And("c>@test",test=12).Or("c==11")
# fx=aggregate()
# fx.select(
#     FullName="concat(FirstName,' ',LastName)"
# )
# import pymongo
# fx=filter("Code=='10001516'")
# item=list(db.get_collection("hrm.Employees").find(fx.get_filter()))
# print item

# db.get_collection("test_001").insert_one({
#     "Code":1
# })
fs=gridfs.GridFS(db)
item=fs.find_one(filter("filename='test'").get_filter())
# ret=fs.put("Hello",filename="test")
 # ObjectId('5af2a9de927e005080821409')
 # fs.find(filter("_id=@id",id=))
x=item

x=item.read()
