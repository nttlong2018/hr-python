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
def employees():
    ret=_db.collection(get_name("hrm.Employees"))
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
    ret = _db.collection(get_name("hrm.Departments"))
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
    ret = _db.collection(get_name("hrm.Positions"))
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
    ret = _db.collection(get_name("hrm.EmployeeTypes"))
    ret.create_unique_index(
        [
            dict(
                field="Code",
                type="string"
            )
        ]
    )
    return ret