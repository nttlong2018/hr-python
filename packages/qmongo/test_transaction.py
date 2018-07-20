import sys

# from packages.mongo.pymongo.read_concern import ReadConcern
#
# from packages.mongo.pymongo.write_concern import WriteConcern


sys.path.append("/home/hcsadmin/argo/packages/mongo")
import pymongo
from pymongo.read_concern import ReadConcern

from pymongo.write_concern import WriteConcern
client = pymongo.MongoClient("localhost", 27017)

session=client.start_session()

# db=session._client.get_database("test")
coll2=client.test.get_collection("test.test004")
coll=client.test.get_collection("test.test003")
session.start_transaction(
    read_concern=ReadConcern("snapshot"),
    write_concern=WriteConcern(w="majority"))

coll2.insert_one({"A":"a01"},session=session)
# coll.insert_one({"code":1},session=session)
# session.abort_transaction()
session.commit_transaction()
session.end_session()
# db=client.get_database("test")
# orders = db.orders
# inventory = db.inventory
# with client.start_session() as session:
#     with session.start_transaction():
#         orders.insert_one({"sku": "abc123", "qty": 100}, session=session)
#         inventory.update_one({"sku": "abc123", "qty": {"$gte": 100}},
#                              {"$inc": {"qty": -100}}, session=session)