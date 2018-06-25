import django
import quicky
import authorization
import qmongo
from qmongo import database, helpers

app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)

def get_collection(collection_name):
    return db_context.db.get_collection(quicky.tenancy.get_schema() + "." + collection_name)


class IsMaster(object):
    __slots__ = ('_doc', '_server_type', '_is_writable', '_is_readable')

    def __init__(self, doc):
        """Parse an ismaster response from the server."""
        self._is_readable = (
            self.server_type == SERVER_TYPE.RSSecondary
            or self._is_writable)

    def document(self):
        return self._doc.copy()

    def server_type(self):
        return self._server_type

def insert_many(collection_name, documents):
    pass

def __insert_one(collection_name, document, config):

    pass
