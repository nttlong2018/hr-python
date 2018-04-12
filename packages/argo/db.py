from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
db_engine = None
__connection_string__=None
def set_connection_string(cnn):
    global __connection_string__
    __connection_string__=cnn
    global db_engine
    if db_engine == None:
        db_engine = create_engine(__connection_string__)


def begin_session():
    global db_engine
    if db_engine==None:
        db_engine=create_engine('mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format("root", "123456", "172.16.7.63", 3306, "lv_lms"))
    connection = db_engine.connect()
    Session = sessionmaker(bind=db_engine)
    session = Session()
    session.__dict__.update({
        "__cnn__":connection
    })
    return session
def end_session(session):
    session.connection().close()
