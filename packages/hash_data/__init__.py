import threading
global lock
lock=threading.Lock()
import uuid
_cache={}
_cache_convert={}
def to_hash(key):
    global _cache
    global _cache_convert
    if _cache.has_key(key):
        return _cache[key]
    else:
        lock.acquire()
        try:
            id=uuid.uuid4().__str__()
            _cache.update({
                key:id
            })
            _cache_convert.update({
                id:key
            })
            lock.release()
            return _cache[key]
        except Exception as ex:
            lock.release()
            raise(ex)
def from_hash(id):
    global _cache_convert
    return _cache_convert.get(id,None)



