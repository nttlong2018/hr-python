from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSSYS_DataDomain():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSSYS_DataDomain",
            "base",
            [["dd_code"]],
            dd_code=helpers.create_field("text",True),
            dd_name=helpers.create_field("text"),
            access_mode=helpers.create_field("numeric"),
            description=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
            detail=helpers.create_field("list",False,dict(
                department_code = helpers.create_field("text"),
                ))
        )
        def on_before_insert(data):
            before_process

        def on_before_update(data):
            before_process(data)

        def before_process(data):
            data.update({
                "detail": [{
                        "department_code":x['department_code'],
                        } for x in data.get('detail',[])]
                })

        helpers.events("HCSSYS_DataDomain").on_before_insert(on_before_insert).on_before_update(on_before_update)
        _hasCreated=True
    ret = db_context.collection("HCSSYS_DataDomain")

    return ret