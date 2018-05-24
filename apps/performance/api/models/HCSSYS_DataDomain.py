from config import database, helpers, db_context

def HCSSYS_DataDomain():
    helpers.validators.set_require_fields(
        "HCSSYS_DataDomain", [
            "dd_code",
            "created_on",
            "created_by"
        ]
    )
    ret = db_context.collection("HCSSYS_DataDomain")
    ret.create_unique_index(
        [
            dict(
                field = "dd_code",
                type = "string"
            )
        ]
    )
    return ret