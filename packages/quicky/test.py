# import mongo
# mongo.set_connection(host="172.16.7.63",user="sys",password="123456",name="test",port=27017)
import expr_tree
fx=expr_tree.Tree()
r = fx.parse("1+1")
print(r)