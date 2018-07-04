#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

import django
import quicky
import authorization
import qmongo
from qmongo import database, helpers
import constant as KEY


app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)

def get_collection(collection_name):
    return db_context.db.get_collection(quicky.tenancy.get_schema() + "." + collection_name)


class Collection(object):
    def __init__(self, collection_name):
        self._collection_name = collection_name
        self._collection = get_collection(collection_name)
        #data not enough primary key
        _config = get_collection(KEY.TABLE_CONFIG).aggregate([
            {
                '$match': { 
                    '$and' : [
                        {'parent_field' : None}, 
                        {'field_path': {'$regex': '^,' + collection_name + ','}},
                        {'is_parent' : False}, 
                    ] 
                }
            },
            {'$project': {'_id': 0}}
        ]);
        self._configs = list(_config)

    #def set_params(self, params):
    #    this._params = params
    #    return self

    #def set_keys(self, keys):
    #    """key: [field1, field2,.etc.]"""
    #    return self

    def is_exists(self, document):
        unique_fields = [a for a in self._configs if a["is_unique"]]
        
        ###data_check: [{key1: value1}, {key2: value2}]
        data_check = []
        for conf in unique_fields:
            data = {}
            data[conf["field_name"]] = document[conf["field_name"]]
            data_check.append(data)

        ret_columns = self._collection.aggregate([
            {
                '$match': { 
                    '$and' : data_check
                }
            }
        ])
        return len(list(ret_columns)) > 0

    def insert_or_update(self, document):
        def _get_key(doc):
            unique_fields = [a for a in self._configs if a["is_unique"]]
            data_key = {}
            for conf in unique_fields:
                data_key[conf["field_name"]] = doc[conf["field_name"]]
            return data_key
        def _insert(doc):
            self._collection.insert_one(doc)
        def _update(doc):
            keys = _get_key(doc)
            self._collection.update_one(
               keys,
               { 
                   '$set' : doc
               }
            )
        def _save(doc):
            check = self.__validate(doc)
            if check["result"]:
                if not self.is_exists(doc):
                    _insert(doc)
                else:
                    _update(doc)

        if type(document) is list:
            for doc in document:
                _save(doc)
        elif type(document) is dict:
            _save(document)
            return check["message"]
        else:
            raise "Document must be a dictionary or a list of dictionary"

    def __validate(self, document):
        "Validate a document in collection"
        #unique_fields = [a for a in self._configs if a["is_unique"]]
        #fields  = [a for a in self._configs if not a["is_unique"]]

        #BEGIN - VALIDATE FIELD
        def validate_field(config):
            f_val = document[conf["field_name"]]
            if not conf["allow_null"] and (not f_val or not f_val.strip()):
                return {
                    'result': False,
                    'message': KEY.MSG_ERROR_NOTNULL.format(conf["field_name"])
                }
            if config["data_type"] == "string":
                #f_val = str(f_val) if not f_val is None else None
                if not config["data_length"] is None and len(f_val) > config["data_length"]:
                    return {
                        'result': False,
                        'message': KEY.MSG_ERROR_LENGTH.format(conf["field_name"], config["data_length"] )
                    }
            elif config["data_type"] == "int":
                if not f_val is None and not type(f_val) is int and not type(f_val) is long:
                    return {
                        'result': False,
                        'message': KEY.MSG_ERROR_DATATYPE.format(conf["field_name"], config["data_type"] )
                    }
            elif config["data_type"] == "float":
                if not f_val is None and not type(f_val) is float:
                    return {
                        'result': False,
                        'message': KEY.MSG_ERROR_DATATYPE.format(conf["field_name"], config["data_type"] )
                    }
            #datatime,etc,...
            return {
                'result': True,
                'message': None
            }

        #END - VALIDATE FIELD

        for conf in self._configs:
            res = validate_field(conf)
            if not res["result"]:
                raise res["message"]

        return {
            'result': True,
            'message': None
        }
