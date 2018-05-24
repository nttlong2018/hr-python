import django
import quicky
import authorization
import qmongo
from qmongo import database
app=quicky.applications.get_app_by_file(__file__)
database=database.connect(app.settings.Database)

def get_list(args):
    items = database.collection("SYS_FunctionList").get_list()
    return items