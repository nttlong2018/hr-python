import logging

from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError, transaction, router
from django.utils import timezone
from django.utils.encoding import force_text

class SessionStore(SessionBase):
    """
    Implements database session store.
    """
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def load(self):
        try:
            s = Session.objects.get(
                session_key=self.session_key,
                expire_date__gt=timezone.now()
            )
            return self.decode(s.session_data)
        except (Session.DoesNotExist, SuspiciousOperation) as e:
            if isinstance(e, SuspiciousOperation):
                logger = logging.getLogger('django.security.%s' %
                        e.__class__.__name__)
                logger.warning(force_text(e))

            import sys
            settings=sys.modules["settings"]
            if not hasattr(settings,"MULTI_TENANCY_DEFAULT_SCHEMA"):
                raise (Exception("It look like you forgot declare 'MULTI_TENANCY_DEFAULT_SCHEMA' in settings.py"))

            self.create(schema=settings.MULTI_TENANCY_DEFAULT_SCHEMA)
            return {}

    def exists(self, session_key):
        return Session.objects.filter(session_key=session_key).exists()

    def create(self, schema = None):
        if schema == None or not type(schema) in [str, unicode]:  # add schema
            import inspect
            fx = inspect.stack()
            error_detail = ""
            for x in fx:
                error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
            raise (
                Exception(
                    "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                        __file__, "SessionStore.create",
                        error_detail
                    )))

        while True:
            self._session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True,schema=schema)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, must_create=False,schema = None):
        """
        Saves the current session data to the database. If 'must_create' is
        True, a database error will be raised if the saving operation doesn't
        create a *new* entry (as opposed to possibly updating an existing
        entry).
        """
        if schema == None:  # add schema
            import inspect
            fx = inspect.stack()
            error_detail = ""
            for x in fx:
                error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
            raise (
                Exception(
                    "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                        __file__, "db.save",
                        error_detail
                    )))

        obj = Session(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(self._get_session(no_load=must_create)),
            expire_date=self.get_expiry_date()
        )
        using = router.db_for_write(Session, instance=obj)
        try:
            with transaction.atomic(using=using):
                obj.save(force_insert=must_create, using=using, schema = schema)
        except IntegrityError:
            if must_create:
                raise CreateError
            raise

    def delete(self, session_key=None,schema = None):
        if schema == None or not type(schema) in [str, unicode]:  # add schema
            import inspect
            fx = inspect.stack()
            error_detail = ""
            for x in fx:
                error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
            raise (
                Exception(
                    "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                        __file__, "SessionStore.delete",
                        error_detail
                    )))

        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            session_obj=Session.objects.get(session_key=session_key)
            session_obj.delete(using=None,schema=schema)
        except Session.DoesNotExist:
            pass

    @classmethod
    def clear_expired(cls):
        Session.objects.filter(expire_date__lt=timezone.now()).delete()


# At bottom to avoid circular import
from django.contrib.sessions.models import Session
