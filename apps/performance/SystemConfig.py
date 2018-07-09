# -*- coding: utf-8 -*-
import threading
from quicky import tenancy
import logging
import datetime
import api.models.HCSSYS_SystemConfig as HCSSYS_SystemConfig
logger = logging.getLogger(__name__)
cache={}
lock=None
global lock
lock=threading.Lock()
_data=dict(
    is_has_number= False,#Numeric
    num_of_number= 1,#Number of characte
    is_has_upper_char= False,#English uppercase characters
    num_of_upper= 1,#Number of characte
    is_has_lower_char= False,#English lowercase characters
    num_of_lower= 1,#Number of characte
    is_has_symbols= False,#Special characters
    num_of_symbol= 1,#Number of character
    created_on= datetime.datetime.now(),
    created_by= "Application",
    modified_on= None,
    modified_by= None,
    is_ad_aut= False,
    session_timeOut= 0,
    time_out_expand= 0,
    minimum_age= 0,
    password_expiration= 30,
    will_expire= False,#Password will expire
    change_after= 30,#Change password after(days)
    apply_minimum_age= True,
    apply_history= False,#Apply password history
    history= 3,#Password history
    apply_minLength= False,#Apply minimum password length
    min_len= 5,#Minimum password length
    apply_maxLength= True,#Apply maximum password lengtH
    max_len= 20,#Maximum password length
    lock_on_failed= False,#Account will be locked on failed login attempts
    threshold_to_lock= 5,#Threshold to lock account
    time_lock= 1,#Account locked in(minutes)
    alert_before= 5,#Alert before(days)
    is_first_change= False,#User must change password at first logon
    not_user_in_password= False,#Don't allow userid in pasword string
    date_format= "dd/MM/yyyy",#định dạng ngày tháng (valuelist LDateFormat)
    dec_place_separator=",", #Ký tự phân cách phần thập phân (Ký tự phân cách)
    dec_place_currency= 2,#Số số lẻ phần thập phân
    default_language= "vi"
           )
class Config():
    def __init__(self):
        for key in _data.keys():
            setattr(self,key,_data[key])
        coll=HCSSYS_SystemConfig()
        data_item=coll.find_one()
        if data_item==None:
            data={}
            for key in self.__dict__.keys():
                if hasattr(self,key):
                    data.update()
            coll.insert_one(_data)
        else:
            for key in data_item.keys():
                if hasattr(self,key):
                    setattr(self,key,data_item[key])

def get():
    global cache
    if cache.has_key(tenancy.get_schema()):
        return cache[tenancy.get_schema()]
    else:
        lock.acquire()
        try:
            cache[tenancy.get_schema()]=Config()
            lock.release()
            return cache[tenancy.get_schema()]
        except Exception as ex:
            lock.release()
            logger.debug(ex)
            raise(ex)

def clear_cache():
    global cache
    lock.acquire()
    try:
        cache[tenancy.get_schema()]=None
        lock.release()
    except Exception as ex:
        lock.release()
        logger.debug(ex)
        raise(ex)