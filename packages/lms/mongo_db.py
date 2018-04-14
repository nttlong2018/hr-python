from pymongo import MongoClient
mongo_client=None
def db():
    global mongo_client
    mongo_client = MongoClient("mongodb://root:123456@172.16.7.63/lv_lms").get_database("lv_lms")
    return mongo_client