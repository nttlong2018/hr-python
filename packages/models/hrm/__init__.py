from qmongo import database
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
def employees():
    ret=create_coll("hrm.employees")
    ret.create_unique_index(
        [
            dict(
                field="Code",
                type="string"
            )
        ],
        [dict(
            field="Username",
            type="string"
        )]
    )
    return ret
def departments():
    ret = create_coll("hrm.departments")
    ret.create_unique_index(
        [
            dict(
                field="Code",
                type="string"
            )
        ]
    )
    return ret
def positions():
    ret = create_coll("hrm.positions")
    ret.create_unique_index(
        [
            dict(
                field="Code",
                type="string"
            )
        ]
    )
    return ret
def employee_types():
    ret =create_coll("hrm.EmployeeTypes")
    ret.create_unique_index(
        [
            dict(
                field="Code",
                type="string"
            )
        ]
    )
    return ret