from .. import models
from .. import common
def get_employee_list_by_department(dept_code, page_size, page_index, sort, search):
    db = common.get_db_context()
    ret = db.system_js.getEmployeeByDepartmentCode(common.get_current_schema(), "PERF", dept_code, page_size, page_index, sort, search)
    return ret

def get_employee_by_employee_code(emp_code):
    ret = {}
    collection = common.get_collection('HCSEM_Employees').aggregate([
        {"$match":{'employee_code':{'$regex':'^'+emp_code}}},
        {"$lookup":{'from':common.get_collection_name_with_schema('HCSSYS_Departments'), 'localField':'department_code', 'foreignField':'department_code', 'as': 'dept'}},
        {"$unwind":{'path':'$dept', "preserveNullAndEmptyArrays":False}},
        {"$project":{
            "photo_id"                     : 1,
            "employee_code"                : 1,
            "last_name"                    : 1,
            "first_name"                   : 1,
            "extra_name"                   : 1,
            "gender"                       : 1,
            "birthday"                     : 1,
            "b_province_code"              : 1,
            "nation_code"                  : 1,
            "ethnic_code"                  : 1,
            "religion_code"                : 1,
            "culture_id"                   : 1,
            "is_retrain"                   : 1,
            "train_level_code"             : 1,
            "marital_code"                 : 1,
            "id_card_no"                   : 1,
            "issued_date"                  : 1,
            "issued_place_code"            : 1,
            "mobile"                       : 1,
            "p_phone"                      : 1,
            "email"                        : 1,
            "personal_email"               : 1,
            "document_no"                  : 1,
            "join_date"                    : 1,
            "official_date"                : 1,
            "career_date"                  : 1,
            "personnel_date"               : 1,
            "emp_type_code"                : 1,
            "labour_type"                  : 1,
            "department_code"              : 1,
            "department_name"              : "$dept.department_name",
            "job_pos_code"                 : 1,
            "job_pos_date"                 : 1,
            "job_w_code"                   : 1,
            "job_w_date"                   : 1,
            "profession_code"              : 1,
            "level_management"             : 1,
            "is_cbcc"                      : 1,
            "is_expert_recruit"            : 1,
            "is_expert_train"              : 1,
            "manager_code"                 : 1,
            "manager_sub_code"             : 1,
            "user_id"                      : 1,
            "job_pos_hold_code"            : 1,
            "job_w_hold_code"              : 1,
            "department_code_hold"         : 1,
            "job_pos_hold_from_date"       : 1,
            "job_pos_hold_to_date"         : 1,
            "end_date"                     : 1,
            "retire_ref_no"                : 1,
            "signed_date"                  : 1,
            "signed_person"                : 1,
            "active"                       : 1,
            "note"                         : 1,
            "p_address"                    : 1,
            "p_province_code"              : 1,
            "p_district_code"              : 1,
            "p_ward_code"                  : 1,
            "p_hamlet_code"                : 1,
            "t_address"                    : 1,
            "t_province_code"              : 1,
            "t_district_code"              : 1,
            "t_ward_code"                  : 1,
            "t_hamlet_code"                : 1,
            "foreigner"                    : 1,
            "vn_foreigner"                 : 1,
            "is_not_reside"                : 1,
            "fo_working"                   : 1,
            "fo_permiss"                   : 1,
            "fo_begin_date"                : 1,
            "fo_end_date"                  : 1
            }}
        ])

    ret = list(collection)[0]

    return ret