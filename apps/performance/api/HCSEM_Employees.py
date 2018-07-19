# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
import logging
import threading
import common
from Query import Employee
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    try:
        ret = {}
        if args['data'] != None:
            searchText = args['data'].get('search', '')
            pageSize = args['data'].get('pageSize', 0)
            pageIndex = args['data'].get('pageIndex', 20)
            sort = args['data'].get('sort', 20)

            pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
            pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

            if args['data'].has_key('where') and args['data']['where'].has_key('department_code'):
                return Employee.get_employee_list_by_department(args['data']['where']['department_code'], pageSize, pageIndex, sort, (lambda x: x.strip() if x != None else "")(searchText))
            else:
                return dict(
                    error = "parameter 'department_code' is not exist"
                )

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def get_employee_by_emp_code(args):
    try:
        ret = {}
        if args['data'] != None:
            if args['data'].has_key('employee_code'):
                ret = Employee.get_employee_by_employee_code(args['data']['employee_code'])
            else:
                return dict(
                    error = "parameter 'employee_code' is not exist"
                )
            return ret

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args['data'])
            ret  =  models.HCSEM_Employees().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args['data'])
            ret  =  models.HCSEM_Employees().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            #if ret['data'].raw_result['updatedExisting'] == True:
            #    ret.update(
            #        item = AdministrativeSubdivisions.get_district().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
            #        )
            lock.release()
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(entity=Employee.get_employee_by_employee_code(args['data']['employee_code']))
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

#def delete(args):
#    try:
#        lock.acquire()
#        ret = {}
#        if args['data'] != None:
#            ret  =  models.HCSEM_Employees().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
#            lock.release()
#            return ret

#        lock.release()
#        return dict(
#            error = "request parameter is not exist"
#        )
#    except Exception as ex:
#        lock.release()
#        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        photo_id                  = common.generate_guid(),
        employee_code             = (lambda x: x['employee_code']             if x.has_key('employee_code')               else None)(args),
        last_name                 = (lambda x: x['last_name']                 if x.has_key('last_name')                   else None)(args),
        first_name                = (lambda x: x['first_name']                if x.has_key('first_name')                  else None)(args),
        extra_name                = (lambda x: x['extra_name']                if x.has_key('extra_name')                  else None)(args),
        gender                    = (lambda x: x['gender']                    if x.has_key('gender')                      else None)(args),
        birthday                  = (lambda x: x['birthday']                  if x.has_key('birthday')                    else None)(args),
        b_province_code           = (lambda x: x['b_province_code']           if x.has_key('b_province_code')             else None)(args),
        nation_code               = (lambda x: x['nation_code']               if x.has_key('nation_code')                 else None)(args),
        ethnic_code               = (lambda x: x['ethnic_code']               if x.has_key('ethnic_code')                 else None)(args),
        religion_code             = (lambda x: x['religion_code']             if x.has_key('religion_code')               else None)(args),
        culture_id                = (lambda x: x['culture_id']                if x.has_key('culture_id')                  else None)(args),
        is_retrain                = (lambda x: x['is_retrain']                if x.has_key('is_retrain')                  else None)(args),
        train_level_code          = (lambda x: x['train_level_code']          if x.has_key('train_level_code')            else None)(args),
        marital_code              = (lambda x: x['marital_code']              if x.has_key('marital_code')                else None)(args),
        id_card_no                = (lambda x: x['id_card_no']                if x.has_key('id_card_no')                  else None)(args),
        issued_date               = (lambda x: x['issued_date']               if x.has_key('issued_date')                 else None)(args),
        issued_place_code         = (lambda x: x['issued_place_code']         if x.has_key('issued_place_code')           else None)(args),
        mobile                    = (lambda x: x['mobile']                    if x.has_key('mobile')                      else None)(args),
        p_phone                   = (lambda x: x['p_phone']                   if x.has_key('p_phone')                     else None)(args),
        email                     = (lambda x: x['email']                     if x.has_key('email')                       else None)(args),
        personal_email            = (lambda x: x['personal_email']            if x.has_key('personal_email')              else None)(args),
        document_no               = (lambda x: x['document_no']               if x.has_key('document_no')                 else None)(args),
        join_date                 = (lambda x: x['join_date']                 if x.has_key('join_date')                   else None)(args),
        official_date             = (lambda x: x['official_date']             if x.has_key('official_date')               else None)(args),
        career_date               = (lambda x: x['career_date']               if x.has_key('career_date')                 else None)(args),
        personnel_date            = (lambda x: x['personnel_date']            if x.has_key('personnel_date')              else None)(args),
        emp_type_code             = (lambda x: x['emp_type_code']             if x.has_key('emp_type_code')               else None)(args),
        labour_type               = (lambda x: x['labour_type']               if x.has_key('labour_type')                 else None)(args),
        department_code           = (lambda x: x['department_code']           if x.has_key('department_code')             else None)(args),
        job_pos_code              = (lambda x: x['job_pos_code']              if x.has_key('job_pos_code')                else None)(args),
        job_pos_date              = (lambda x: x['job_pos_date']              if x.has_key('job_pos_date')                else None)(args),
        job_w_code                = (lambda x: x['job_w_code']                if x.has_key('job_w_code')                  else None)(args),
        job_w_date                = (lambda x: x['job_w_date']                if x.has_key('job_w_date')                  else None)(args),
        profession_code           = (lambda x: x['profession_code']           if x.has_key('profession_code')             else None)(args),
        level_management          = (lambda x: x['level_management']          if x.has_key('level_management')            else None)(args),
        is_cbcc                   = (lambda x: x['is_cbcc']                   if x.has_key('is_cbcc')                     else None)(args),
        is_expert_recruit         = (lambda x: x['is_expert_recruit']         if x.has_key('is_expert_recruit')           else None)(args),
        is_expert_train           = (lambda x: x['is_expert_train']           if x.has_key('is_expert_train')             else None)(args),
        manager_code              = (lambda x: x['manager_code']              if x.has_key('manager_code')                else None)(args),
        manager_sub_code          = (lambda x: x['manager_sub_code']          if x.has_key('manager_sub_code')            else None)(args),
        user_id                   = (lambda x: x['user_id']                   if x.has_key('user_id')                     else None)(args),
        job_pos_hold_code         = (lambda x: x['job_pos_hold_code']         if x.has_key('job_pos_hold_code')           else None)(args),
        job_w_hold_code           = (lambda x: x['job_w_hold_code']           if x.has_key('job_w_hold_code')             else None)(args),
        department_code_hold      = (lambda x: x['department_code_hold']      if x.has_key('department_code_hold')        else None)(args),
        job_pos_hold_from_date    = (lambda x: x['job_pos_hold_from_date']    if x.has_key('job_pos_hold_from_date')      else None)(args),
        job_pos_hold_to_date      = (lambda x: x['job_pos_hold_to_date']      if x.has_key('job_pos_hold_to_date')        else None)(args),
        end_date                  = (lambda x: x['end_date']                  if x.has_key('end_date')                    else None)(args),
        retire_ref_no             = (lambda x: x['retire_ref_no']             if x.has_key('retire_ref_no')               else None)(args),
        signed_date               = (lambda x: x['signed_date']               if x.has_key('signed_date')                 else None)(args),
        signed_person             = (lambda x: x['signed_person']             if x.has_key('signed_person')               else None)(args),
        active                    = (lambda x: x['active']                    if x.has_key('active')                      else None)(args),
        note                      = (lambda x: x['note']                      if x.has_key('note')                        else None)(args),
        p_address                 = (lambda x: x['p_address']                 if x.has_key('p_address')                   else None)(args),
        p_province_code           = (lambda x: x['p_province_code']           if x.has_key('p_province_code')             else None)(args),
        p_district_code           = (lambda x: x['p_district_code']           if x.has_key('p_district_code')             else None)(args),
        p_ward_code               = (lambda x: x['p_ward_code']               if x.has_key('p_ward_code')                 else None)(args),
        p_hamlet_code             = (lambda x: x['p_hamlet_code']             if x.has_key('p_hamlet_code')               else None)(args),
        t_address                 = (lambda x: x['t_address']                 if x.has_key('t_address')                   else None)(args),
        t_province_code           = (lambda x: x['t_province_code']           if x.has_key('t_province_code')             else None)(args),
        t_district_code           = (lambda x: x['t_district_code']           if x.has_key('t_district_code')             else None)(args),
        t_ward_code               = (lambda x: x['t_ward_code']               if x.has_key('t_ward_code')                 else None)(args),
        t_hamlet_code             = (lambda x: x['t_hamlet_code']             if x.has_key('t_hamlet_code')               else None)(args),
        foreigner                 = (lambda x: x['foreigner']                 if x.has_key('foreigner')                   else None)(args),
        vn_foreigner              = (lambda x: x['vn_foreigner']              if x.has_key('vn_foreigner')                else None)(args),
        is_not_reside             = (lambda x: x['is_not_reside']             if x.has_key('is_not_reside')               else None)(args),
        fo_working                = (lambda x: x['fo_working']                if x.has_key('fo_working')                  else None)(args),
        fo_permiss                = (lambda x: x['fo_permiss']                if x.has_key('fo_permiss')                  else None)(args),
        fo_begin_date             = (lambda x: x['fo_begin_date']             if x.has_key('fo_begin_date')               else None)(args),
        fo_end_date               = (lambda x: x['fo_end_date']               if x.has_key('fo_end_date')                 else None)(args)
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['employee_code']
    del ret_dict['photo_id']
    return ret_dict