import sys
class OpenFile(object):
    def __init__(self, path):
        self._path = path
        
    def __enter__(self):
        try:
            self._f = open(self._path)
            return self._f
        except FileNotFoundError as _:
            print('get it and exit')
            sys.exit(1)
    
    def __exit__(self, exc_type, exc_value, exc_trace):
        if hasattr(self, '_f'):
        	self._f.close()
            

with OpenFile('dong.txt') as f:
    f.readlines()