import os
import sys
def load_paths(path):
    lst= os.walk(path).next()
    root_path=lst[0]
    for item in lst[1]:
        _path=root_path+"/"+item
        sys.path.append(_path)
        if os.path.isdir(_path):
            load_paths(_path)




