from models.HCSSYS_DataDomain import HCSSYS_DataDomain

def get_list(args):
    items = HCSSYS_DataDomain().get_list()
    return items