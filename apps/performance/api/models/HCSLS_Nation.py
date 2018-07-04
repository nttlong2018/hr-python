from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Nation():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Nation",
            "base",
            [["nation_code"]],
            nation_code=helpers.create_field("text", True),
            nation_name=helpers.create_field("text", True),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            continents=helpers.create_field("numeric"),
            #eat_amount=helpers.create_field("numeric"),
            #home_amount=helpers.create_field("numeric"),
            #taxi_amount=helpers.create_field("numeric"),
            #sub_days_amount=helpers.create_field("numeric"),
            nation_name2=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
            #department_code=helpers.create_field("text"),
            org_nation_code=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Nation")

    return ret