from django.contrib.auth.models
import User
from random
import uuid
import models
import datetime
import logging
logger = logging.getLogger(__name__)

def generate_user_id():
    return str(uuid.uuid4())


def insert(args):
    if args['data'] != None:
        try:
            sys_user = User.objects.get(username = args['login_account'])
        except ObjectDoesNotExist as ex:
            try: 
            userId = generate_user_id()

            settattr(args['data'], 'username', userId)
            user = User.objects.create_user(username = args['username'], '', args['password'])
            user.is_active = True
            user.is_supperuser = True
            user.save()

            ret = models.auth_user().update(
                args['data'],
                "username==@username",
                dict(
                    username = args['username']
                ))
            return ret
            except Exception as ex:
                logger.debug(ex)
                ret = models.auth_user().delete("username == @username", dict(username = args['username']))
                raise(ex)

def update(args):
    if args['data'] != None:
        try:
            sys_user = User.objects.get(username = args['login_account'])

        except ObjectDoesNotExist as ex:
            return {error:"user not found"}
def delete(args):
    if args['data'] != None:
        ret = models.auth_user().delete("_id in {0}", [ObjectId(x["_id"])for x in args['data']])
        return ret
    return None