from config import database, helpers, db_context
import datetime
_hasCreated=False

def HCSSYS_ComboboxList():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSSYS_ComboboxList",
            "base",
            [["combobox_code"]],
            combobox_code = helpers.create_field("text",True),
            language=helpers.create_field("text", True),
            display_name=helpers.create_field("text"),
            description=helpers.create_field("text"),
            table_name=helpers.create_field("text"),
            table_fields=helpers.create_field("list"),
            display_fields=helpers.create_field("list"),
            predicate=helpers.create_field("list", False, dict(
                column = helpers.create_field("string"),
                operator = helpers.create_field("string")
                )),
            value_field=helpers.create_field("text"),
            caption_field=helpers.create_field("text"),
            sorting_field=helpers.create_field("object"),
            filter_field=helpers.create_field("text"),
            multi_select=helpers.create_field("bool"),
            page_size=helpers.create_field("int"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
        )

        _hasCreated=True
    ret = db_context.collection("HCSSYS_ComboboxList")

    return ret