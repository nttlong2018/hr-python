class model_event():
    """
    This a class hold event of model, each model has an instance of model_event
    """
    def __init__(self):
        self._on_before_insert = []
        self._on_after_insert = []
        self._on_before_update = []
        self._on_after_update = []
    def on_before_insert(self,callback):
        # type: (function) -> model_event
        """
                Attach on before insert event
                callback is a function with dict param. The data will be insert
                :param callback:the function in which perform source code before data insert into mongodb storage
                :return:
        """
        self._on_before_insert.append(callback)
        return self
    def on_after_insert(self,callback):
        """
               Attach on after before insert event
               callback is a function with dict param. The data has been inserted
               :param callback:the function in which perform source code after data insert into mongodb storage
               :return:
               """
        self._on_after_insert.append(callback)
        return self
    def on_before_update(self,callback):
        """
               Attach on before update event
               callback is a function with dict param. The data will be update
               :param callback:the function in which perform source code before data update into mongodb storage
               :return:
               """
        self._on_before_update.append(callback)
        return self
    def on_after_update(self,callback):
        """
                       Attach on after update event
                       callback is a function with dict param. The data has been updated
                       :param callback:the function in which perform source code after data update into mongodb storage
                       :return:
                       """
        self._on_after_update.append(callback)
        return self

