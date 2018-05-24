import django
import quicky
import authorization
import qmongo
from qmongo import database, helpers
app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)