# -*- coding: utf-8 -*-
import sys

# from packages.mongo.pymongo.read_concern import ReadConcern
#
# from packages.mongo.pymongo.write_concern import WriteConcern

# Đặt đường dẫn để import thư viện pymong có hỗ trợ transaction
sys.path.append("/home/hcsadmin/argo/packages/mongo")
#import qmongo
import transaction
import helpers
import database
# connect to database lưu ý phải là mongodb 4.0
db=database.connect(host="localhost",port=27017,name="test",user="root",password="123456")
# Định nghĩa model
helpers.define_model(
    "test",
    [["Code"]],
    Code=helpers.create_field("text",True))
# tạo collection
coll=db.collection("test")
# Test nên kg cần schema, tắt đi
coll.turn_never_use_schema_on()
# Tạo session
session=transaction.create_session(coll)
# Bắt đầu transaction từ session vừa tạo
transaction.start_transaction(session)
# cho collection join vào session (tất cả các collection đều phải tham gia vào session, trong ví dụ này chỉ có 1)
coll.set_session(session)
# Thêm một dòng vào collection
coll.insert(
    {
        "Code":"0001"
    }
)

items_from_aggregate=coll.aggregate().get_list()
items_from_coll=coll.get_list()

print(items_from_aggregate)
print(items_from_coll)
# Rollback coi như chưa insert dữ liệu vào
transaction.abort_transaction(session)

# đóng session
transaction.end_session(session)

# import pymongo
# from pymongo.read_concern import ReadConcern
#
# from pymongo.write_concern import WriteConcern
#
# client = pymongo.MongoClient("localhost", 27017)
#
# session=client.start_session()
#
# # db=session._client.get_database("test")
# coll2=client.test.get_collection("test.test004")
# coll=client.test.get_collection("test.test003")
# session.start_transaction(
#     read_concern=ReadConcern("snapshot"),
#     write_concern=WriteConcern(w="majority"))
#
# coll2.insert_one({"A":"a01"},session=session)
# # coll.insert_one({"code":1},session=session)
# # session.abort_transaction()
# session.commit_transaction()
# session.end_session()
# db=client.get_database("test")
# orders = db.orders
# inventory = db.inventory
# with client.start_session() as session:
#     with session.start_transaction():
#         orders.insert_one({"sku": "abc123", "qty": 100}, session=session)
#         inventory.update_one({"sku": "abc123", "qty": {"$gte": 100}},
#                              {"$inc": {"qty": -100}}, session=session)