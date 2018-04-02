from django.http import HttpResponse
from django.shortcuts import redirect
import argo

application=argo.get_application(__file__)

@argo.template("index.html")
def index(request):
    return  application.render(request)