import datetime
from enum import Enum
class error_types(Enum):
    NONE=0
    DUPLICATE=1
    NOTFOUND=2
    INVALID=3
class exception(Exception):
    def __init__(self):
        self.types = error_types.NONE
        self.fields = []
        self.message = ""
class base:
    def __init__(self):
        self.createdOn = datetime.datetime.now()
        self.createOnUTC = datetime.datetime.utcnow()
        self.modifiedOn = None
        self.modifiedOnUTC = None
        self.createdBy = "application"
        self.modifiedBy = "application"
        self.description = ""
class user(base):
    userId=None
    def __init__(self):
        base.__init__(self)
        self.displayName=""
        self.username=""
        self.email=""
        self.totalLogin=0
        self.totalLoginFail=0
        self.latestLoginOn=None
        self.latestLoginFail=None
        self.isSysAdmin=False
class sigin_info:
    def __init__(self):
        self.token=""
        self.siginOn=None
        self.siginOnUtc=None
        self.username=None
        self.user=None
        self.userId=None
        self.language=None

