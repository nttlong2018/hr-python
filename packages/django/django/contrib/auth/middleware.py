from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject


def get_user(request, schema = None):
    if schema == None or not type(schema) in [str, unicode]:  # add schema
        import inspect
        fx = inspect.stack()
        error_detail = ""
        for x in fx:
            error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
        raise (
            Exception(
                "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                    __file__, "get_user",
                    error_detail
                )))
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request,schema=schema)
        setattr(request._cached_user,"schema",schema)
    return request._cached_user


class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        import threading
        import sys
        settings=sys.modules["settings"]
        ct=threading.currentThread()
        schema=settings.MULTI_TENANCY_DEFAULT_SCHEMA
        if hasattr(ct,"tenancy_code"):
            schema=ct.tenancy_code
        request.user = SimpleLazyObject(lambda: get_user(request,schema=schema))


class RemoteUserMiddleware(object):
    """
    Middleware for utilizing Web-server-provided authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate the username passed in the ``REMOTE_USER`` request header.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.

    The header used is configurable and defaults to ``REMOTE_USER``.  Subclass
    this class and change the ``header`` attribute if you need to use a
    different header.
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "REMOTE_USER"

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                self._remove_invalid_user(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.get_username() == self.clean_username(username, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(remote_user=username)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError:  # Backend has no clean_username method.
            pass
        return username

    def _remove_invalid_user(self, request):
        """
        Removes the current authenticated user in the request which is invalid
        but only if the user is authenticated via the RemoteUserBackend.
        """
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ''))
        except ImproperlyConfigured:
            # backend failed to load
            auth.logout(request)
        else:
            if isinstance(stored_backend, RemoteUserBackend):
                auth.logout(request)
