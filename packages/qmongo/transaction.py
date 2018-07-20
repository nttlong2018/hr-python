import database
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
def create_session(coll):
    if not isinstance(coll,database.COLL):
        raise (Exception("It looks like you create session from instance is not 'qmongo.database.COLL'"))
    txt_version =coll.qr.db.eval("return db.version()").split('.')[0]
    if int(txt_version.split('.')[0])<4:
        raise (Exception("Your mongodb verion is '{0}' not support 'transaction'".format(txt_version)))

    session = coll.qr.db.client.start_session()
    return session
def start_transaction(session):
    session.start_transaction(
        read_concern=ReadConcern("snapshot"),
        write_concern=WriteConcern(w="majority"))
    return session
def abort_transaction(session):
    session.abort_transaction()
    return  session
def end_session(session):
    session.end_session()
def commit_transaction(session):
    session.commit_transaction()