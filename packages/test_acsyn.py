import async.caller
import time
from multiprocessing import Pool

def test():
    time.sleep(2)
    print "OK"

def xong():
    print "xong roi"

runner=async.caller.AsyncCall(test)
runner.__call__()
print "xong"