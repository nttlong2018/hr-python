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

def set_config(*args,**kwargs):
    global __connection_string__
    if args==():
        args=kwargs
    print kwargs
    if type(args) is tuple:
        args=args[0]
    db_engine=args["engine"]
    db_user = args["user"]
    db_password = args["password"]
    db_host = args["host"]
    db_port = args["port"]
    db_name = args["name"]
    __connection_string__='{5}://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_user, db_password, db_host, db_port, db_name,db_engine)
def begin_session(args):
    _db_engine = args["engine"]
    _db_user = args["user"]
    _db_password = args["password"]
    _db_host = args["host"]
    _db_port = args["port"]
    _db_name = args["name"]
    str_cnn = '{5}://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(_db_user, _db_password, _db_host, _db_port,
                                                              _db_name, _db_engine)
    db_engine = create_engine(str_cnn)
    connection = db_engine.connect()
    Session = sessionmaker(bind=db_engine)
    session = Session()
    session.__dict__.update({
        "__cnn__":connection
    })
    return session
def end_session(session):
    session.connection().close()