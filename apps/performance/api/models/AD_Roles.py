from config import database, helpers, db_context
import datetime
_hasCreated=False

def AD_Roles():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "AD_Roles",
            "base",
            [["role_code"]],
            role_code = helpers.create_field("text",True),
            role_name=helpers.create_field("text",True),
            dd_code=helpers.create_field("text",True),
            description=helpers.create_field("text"),
            stop=helpers.create_field("bool"),
            #role_type=helpers.create_field("text",True),
            #is_system=helpers.create_field("bool"),
            #administrator=helpers.create_field("numeric"),
            #system_admin=helpers.create_field("numeric"),
            #function_admin=helpers.create_field("text"),
            #security_level=helpers.create_field("text"),
            #start_date=helpers.create_field("date"),
            #end_date=helpers.create_field("text"),
            #note=helpers.create_field("date"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )

        _hasCreated=True
    ret = db_context.collection("AD_Roles")

    return ret