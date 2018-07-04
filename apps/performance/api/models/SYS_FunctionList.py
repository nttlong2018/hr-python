from config import database, helpers, db_context
_hasCreated=False
def SYS_FunctionList():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "SYS_FunctionList",
            [["function_id"]],
            sorting=helpers.create_field("text"),
            description=helpers.create_field("text"),
            custom_name=helpers.create_field("text"),
            style_class=helpers.create_field("text"),
            url=helpers.create_field("text"),
            image=helpers.create_field("text"),
            default_name=helpers.create_field("text", True),
            height=helpers.create_field("text"),
            parent_id=helpers.create_field("text"),
            active=helpers.create_field("bool"),
            function_id=helpers.create_field("text", True),
            type=helpers.create_field("text"),
            width=helpers.create_field("text"),
            icon=helpers.create_field("text"),
            app=helpers.create_field("text"),
            level_code=helpers.create_field("list")
        )
        _hasCreated=True
    ret = db_context.collection("SYS_FunctionList")

    return ret