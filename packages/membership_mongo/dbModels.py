from  membership import  models
import datetime
def upper_first(txt):
    return  txt[0].upper()+txt[1:txt.__len__()]
def lower_first(txt):
    return txt[0].lower() + txt[1:txt.__len__()]
def load_data_from_dict(instance,_dict):
    for key in instance.__dict__.keys():
        instance.__dict__.update({
            key:_dict.get(upper_first(key),None)
        })
    return instance
class base:
    def __init__(self):

        self.CreatedOn=datetime.datetime.now()
        self.CreatedOnUTC=datetime.datetime.utcnow()
        self.CreatedBy="application"
        self.ModifiedOn=None
        self.ModifiedOnUTC=None
        self.Description=None

    def apply(self,_model):
        for key in user_model.__dict__.keys():
            self.__dict__.update({
                upper_first(key): _model.get(key)
            })
    def tranfer_data_to(self,_model):
        for key in _model.__dict__.keys():
            if key!="_id":
                _model.__dict__.update({key:self.__dict__.get(upper_first(key))})
        return _model


class users(base):
    def __init__(self):
        base.__init__(self)
        self.PasswordSalt=""
        self.Password=""
        self.Username=""
        self.Email=None
        self.IsActive=False
        self.ActivationOn=None
        self.ActivationOnUTC = None

        self.TotalLogin = 9
        self.TotalLoginFail = 0
        self.LatestLogin = None
        self.LatestLoginFail = None



