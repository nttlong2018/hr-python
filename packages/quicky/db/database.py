import expr

from pymongo import MongoClient
from pymongo.errors import OperationFailure
import logging
logger = logging.getLogger(__name__)
_db={}
