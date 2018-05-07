
from beaker.util import machine_identifier

from  . import models
from . import mongo_db
def get_list():
    session=db.begin_session()
    ret_list=list(session.query(models.course_overviews_courseoverview))
    db.end_session(session)
    return ret_list
def delete_by_id(id):
    session = db.begin_session()
    get_all_items_clause=session.query(models.course_overviews_courseoverviewtab).filter(models.course_overviews_courseoverviewtab.course_overview_id==id)
    [session.delete(x) for x in get_all_items_clause.all()]

    delete_item=session.query(models.course_overviews_courseoverview).get(id)
    if delete_item!=None:
        session.delete(delete_item)
    session.commit()
    db.end_session(session)
    items=id.split(":")[1].split("+")
    md_item=mongo_db.db().get_collection("modulestore.active_versions").find_one({
                        "run": items[2],
                        "org": items[0],
                        "course": items[1]
                    })
    if md_item!=None:

        draftBranch = md_item["versions"]["draft-branch"]
        publishedBranch = md_item["versions"]["published-branch"]
        mongo_db.db().get_collection("modulestore.structures").remove({ "_id": draftBranch })
        mongo_db.db().get_collection("modulestore.structures").remove({ "_id": publishedBranch })
        mongo_db.db().get_collection("modulestore.active_versions").remove({ "_id": md_item["_id"] })





    return md_item