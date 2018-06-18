from config import database, helpers, db_context
import datetime
_hasCreated=False
def HCSSYS_CollectionInfo():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSSYS_CollectionInfo",
            "base",
            [],
            table_name = helpers.create_field("text",True),
            field_name=helpers.create_field("text",True),
            data_type=helpers.create_field("text",True),
            data_length=helpers.create_field("numeric"),
            default_value=helpers.create_field("text"),
            is_unique=helpers.create_field("bool"),
            description=helpers.create_field("text"),
            is_parent=helpers.create_field("bool"),
            parent_field=helpers.create_field("text"),
            field_path=helpers.create_field("text", True),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSSYS_CollectionInfo")
    return ret
