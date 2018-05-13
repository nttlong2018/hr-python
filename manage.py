#!/usr/bin/env python
import os
import sys

REPO_PATH=os.path.dirname(os.path.realpath(__file__))

sys.path.append(REPO_PATH +os.sep+"apps")
sys.path.append(REPO_PATH+os.sep+"packages")
sys.path.append(REPO_PATH+os.sep+"packages/django")


if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line
    import django

    # django.setup()

    execute_from_command_line(sys.argv)
