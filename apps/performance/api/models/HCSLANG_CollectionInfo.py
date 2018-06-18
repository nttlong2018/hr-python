from config import database, helpers, db_context
import datetime
_hasCreated=False
def HCSLANG_CollectionInfo():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLANG_CollectionInfo",
            "base",
            [],
            language = helpers.create_field("text",True),
            field_path=helpers.create_field("text",True),
            default_caption=helpers.create_field("text",True),
            custom_caption=helpers.create_field("text"),

            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLANG_CollectionInfo")
    return ret

