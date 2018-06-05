class model_event():
    def __init__(self):
        self._on_before_insert = []
        self._on_after_insert = []
        self._on_before_update = []
        self._on_after_update = []
    def on_before_insert(self,callback):
        self._on_before_insert.append(callback)
        return self
    def on_after_insert(self,callback):
        self._on_after_insert.append(callback)
        return self
    def on_before_update(self,callback):
        self._on_before_update.append(callback)
        return self
    def on_after_update(self,callback):
        self._on_after_update.append(callback)
        return self

