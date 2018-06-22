from config import database, helpers, db_context
_hasCreated=False

def tmp_transactions():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "tmp_transactions",
            [["transaction_id"]],
            transaction_id=helpers.create_field("text", True),
            collection_name=heplers.create_field("text", True),
            path=helpers.create_field("text", True),
            session=helpers.create_field("text", True),
            ordinal=helpers.create_field("numeric"),
            data=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
        )
        _hasCreated=True
    ret = db_context.collection("tmp_transactions")

    return ret