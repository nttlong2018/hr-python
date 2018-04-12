from argo import db
from  . import models
def get_list():
    session=db.begin_session()
    ret_list=list(session.query(models.course_overviews_courseoverview))
    db.end_session(session)
    return ret_list