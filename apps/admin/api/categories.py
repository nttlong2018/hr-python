import quicky
import admin.forms as admin_form
app=quicky.applications.get_app_by_file(__file__)
db=quicky.db.database.connect(app.settings.Database)
def get_list(params):
    frm=getattr(admin_form,params["data"]["path"])
    if frm==None:
        raise Exception("form was not found")
    coll_name=frm.layout.get_config()["collection"]
    coll=db.collection(coll_name).aggregate()
    project={}
    for item in frm.layout.get_table_columns():
        project.update({
            item["name"]:1
        })
    count=coll.copy()
    count.count("totalItems")
    coll.project(project)
    items= coll.get_list()
    return dict(
        items=items,
        totalItem=count.get_item()["totalItems"],
        pageIndex=0,
        pageSize=20
    )

