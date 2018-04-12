import argo
def get_list():
    list=argo.membership.find("sys",0,50)
    return list