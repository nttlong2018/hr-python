from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_TrainSupplier():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_TrainSupplier",
            "base",
            [["tr_supplier_code"]],
            tr_supplier_code=helpers.create_field("text", True),
            tr_supplier_name=helpers.create_field("text", True),
            tr_supplier_name2=helpers.create_field("text"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
            #department_code=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_TrainSupplier")

    return ret