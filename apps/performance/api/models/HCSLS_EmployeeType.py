from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSLS_EmployeeType():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_EmployeeType",
            "base",
            [["emp_type_code"]],
            emp_type_code=helpers.create_field("text", True),
            emp_type_name=helpers.create_field("text", True),
            emp_type_name2=helpers.create_field("text"),
            rate_main_sal=helpers.create_field("numeric"),
            rate_soft_sal=helpers.create_field("numeric"),
            true_type=helpers.create_field("numeric", True),
            # probation_time_by=helpers.create_field("numeric"),
            # probation_time=helpers.create_field("text"),
            # is_fix=helpers.create_field("numeric"),
            # coeff=helpers.create_field("text"),
            # begin_date_cal=helpers.create_field("numeric"),
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
    ret = db_context.collection("HCSLS_EmployeeType")

    return ret