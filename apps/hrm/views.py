import argo
@argo.template("index.html")
def index(request):
    return request.render({})