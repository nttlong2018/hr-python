from qmongo import database
from qmongo import helpers
_db=None
_prefix=None
def connect(*args,**kwargs):
    global _db
    if _db==None:
        _db=database.connect(*args,**kwargs)
def set_prefix(prefix):
    global _prefix
    _prefix=prefix
def get_name(name):
    global _prefix
    if _prefix==None:
        return name
    else:
        return _prefix+"."+name
def create_coll(name):
    global _db
    if _db==None:
        raise (Exception("The database was not init"))
    return _db.collection(get_name(name))
def provinces():
    ret=create_coll("hrm.provinces")
    ret.create_unique_index(
        [
            dict(
                field="Code",
                type="string"
            )
        ]
    )
    return ret
def districts():
    ret=create_coll("hrm.districts")
    ret.create_unique_index(
        [
            dict(
                field="Code",
                type="string"
            )
        ]
    )
    return ret

helpers.validators.set_require_fields(
    get_name("hrm.provinces"),
    [
        "Code",
        "Name"
    ])
helpers.validators.set_require_fields(
    get_name("hrm.districts"),
    [
        "Code",
        "Name",
        "ProvinceCode"
    ])

