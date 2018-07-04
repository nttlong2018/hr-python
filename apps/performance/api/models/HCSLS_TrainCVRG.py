from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_TrainCVRG():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_TrainCVRG",
            "base",
            [["train_cvrg_code"]],
            train_cvrg_code=helpers.create_field("text", True),
            train_cvrg_name=helpers.create_field("text", True),
            train_cvrg_name2=helpers.create_field("text"),
            #is_lang=helpers.create_field("bool"),
            #is_bhld=helpers.create_field("bool"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            domain_code=helpers.create_field("text", True),
            lock=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_TrainCVRG")

    return ret