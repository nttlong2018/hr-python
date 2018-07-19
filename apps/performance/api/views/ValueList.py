from qmongo import qview
from .. import models

def ValueList():
    return qview.create_mongodb_view(
        models.SYS_ValueList().aggregate().unwind("values")
        ,
        "View_ValueList"
        )
