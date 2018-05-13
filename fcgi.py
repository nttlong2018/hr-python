import logging
logger=logging.getLogger(__name__)
try:
    import manage
    import os
    from subprocess import call
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as ex:
    logger.debug(ex)

