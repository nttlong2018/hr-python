import manage
import os
from subprocess import call
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
call('python {0}/manage.py runserver 127.0.0.1:8000'.format(os.getcwd()))