# -*- coding: utf-8 -*-
from config import database, helpers, db_context
_hasCreated=False
def HCSSYS_ExcelTemplate():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSSYS_ExcelTemplate",
            "base",
            [["function_id"], ["template_code"], ["detail.field_name", "template_code"]],
            function_id=helpers.create_field("text", True),
            template_code=helpers.create_field("text", True),
            template_name=helpers.create_field("text", True),
            is_default=helpers.create_field("bool"),
            view_name=helpers.create_field("text", True),
            detail=helpers.create_field("list",False,dict(
                field_name = helpers.create_field("text"),
                lookup_data = helpers.create_field("text"),
                lookup_key_field = helpers.create_field("text"),
                lookup_result = helpers.create_field("text"),
                allow_null = helpers.create_field("bool"),
                is_key = helpers.create_field("bool"),
                language = helpers.create_field("text"),
                header_text = helpers.create_field("text"),
                is_visible = helpers.create_field("bool"),
                ordinal = helpers.create_field("numeric")
                )),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSSYS_ExcelTemplate")

    return ret