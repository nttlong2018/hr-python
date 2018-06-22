
import quicky
import performance.api.models as models


def get_collection(collection_name):
    return models.db_context.db.get_collection(quicky.tenancy.get_schema() + "." + collection_name)