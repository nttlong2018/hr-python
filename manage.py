#!/usr/bin/env python
import os
import sys

REPO_PATH=os.path.dirname(os.path.realpath(__file__))
sys.path.append(REPO_PATH +"/apps")
sys.path.append(REPO_PATH+"/packages")
import argo
argo.config.load_settings("default")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "default")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)