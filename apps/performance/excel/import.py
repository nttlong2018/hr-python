from django.http import HttpResponse
import quicky
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import load_workbook
import datetime
import base64
from io import BytesIO


def call(args):
    wb = load_workbook(filename=BytesIO(base64.b64decode(args["data"]["_content"])))

    return args["data"];
