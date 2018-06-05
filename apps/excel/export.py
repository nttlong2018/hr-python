#from django.http import HttpResponse
import quicky
#from openpyxl import Workbook
#from openpyxl.writer.excel import save_virtual_workbook
#import datetime

@quicky.view.template("")
def call(request):
    pass
    #workbook = Workbook()
    #worksheet = workbook.active
    ## Data can be assigned directly to cells
    #worksheet['A1'] = 42

    ## Rows can also be appended
    #worksheet.append([1, 2, 3])

    ## Python types will automatically be converted
    
    #worksheet['A2'] = datetime.datetime.now()

    #response = HttpResponse(content=save_virtual_workbook(workbook), mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #response['Content-Disposition'] = 'attachment; filename=myexport.xlsx'
    #return response
