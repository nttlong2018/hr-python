import openpyxl
from openpyxl.styles import Font

worksheet_style = {
        'NORMAL' : "STYLE_NORMAL" 
    }

class format_style():
    def __init__(self, style):
        self.__style = style

    def format(self, worksheet):
        "Format your worksheet in Excel with Styles"
        if(self.__style == worksheet_style["NORMAL"]):
            return self.__format_normal(worksheet)
        else:
            return worksheet

    def __format_normal(self, worksheet):
        "Format your worksheet in Excel with NORMAL Style"
        red_font = Font(color='00FF0000', italic=True, bold=True)
        for cell in worksheet["1:1"]:
            cell.font = red_font
        return worksheet

