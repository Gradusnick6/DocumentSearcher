from multiprocessing.managers import BaseManager


class MultiProcessManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.__is_started = False

    def start(self, **kwargs):
        if not self.__is_started:
            super().start()
            self.__is_started = True

    def shutdown(self):
        if self.__is_started:
            super().shutdown()
            self.__is_started = False
