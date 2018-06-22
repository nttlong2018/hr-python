# -*- coding: utf-8 -*-
from config import database, helpers, db_context
_hasCreated=False
def HCSSYS_Departments():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSSYS_Departments",
            "base",
            [["department_code"]],
            #id=helpers.create_field("numeric",True),
            department_code=helpers.create_field("text", True),
            department_name=helpers.create_field("text", True),
            department_name2=helpers.create_field("text"),
            department_alias=helpers.create_field("text"),
            #parent_id=helpers.create_field("numeric"),
            parent_code=helpers.create_field("text"),
            level=helpers.create_field("numeric"),
            level_code=helpers.create_field("list"),
            #level_code2=helpers.create_field("text"),
            department_tel=helpers.create_field("text"),
            department_fax=helpers.create_field("text"),
            department_email=helpers.create_field("text"),
            department_address=helpers.create_field("text"),
            #Xem lại kiểu dữ liệu
            nation_code=helpers.create_field("text"),
            province_code=helpers.create_field("text"),
            district_code=helpers.create_field("text"),
            is_company=helpers.create_field("bool"),
            is_fund=helpers.create_field("bool"),
            is_fund_bonus=helpers.create_field("bool"),
            decision_no=helpers.create_field("text"),
            decision_date=helpers.create_field("date"),
            effect_date=helpers.create_field("date"),
            license_no=helpers.create_field("text"),
            tax_code=helpers.create_field("text"),
            lock_date=helpers.create_field("date"),
            logo_image=helpers.create_field("text"),
            manager_code=helpers.create_field("text"),
            secretary_code=helpers.create_field("text"),
            ordinal=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            note=helpers.create_field("text"),
            region_code=helpers.create_field("text"),
            domain_code=helpers.create_field("text"),
            signed_by=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSSYS_Departments")

    return ret