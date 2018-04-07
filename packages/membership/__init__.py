"dasdasda dasdas dasdasd "
import importlib
import inspect
from . import models
def set_connection_string(strConn):
    fn=getattr(_membership_instance,inspect.stack()[0][3])
    fn(strConn)
def get_connection_string():
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return  fn()
def set_provider(name):
    global _membership_instance
    _membership_instance=importlib.import_module(name)
def set_config(config):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    fn(config)
def validate_account(username,password):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(username,password)
def create_user(username,password,email):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(username, password,email)
def sign_in(username,sessionId,language):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(username,sessionId,language)
def validate_session(sessionId):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(sessionId)
def active_user(username):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(username)
def get_user(username):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(username)
def sign_out(sessin_id):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(sessin_id)
def change_password(username,password):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(username,password)
def find(search_text,page_index,page_size):
    fn = getattr(_membership_instance, inspect.stack()[0][3])
    return fn(search_text,page_index,page_size)

