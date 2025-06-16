from multiprocessing.managers import BaseManager
from Model.Service.ProgressBar.ProcessStatus import ProcessStatus


class ProgressBar:
    def __init__(self, max_value=None):
        """
        :param max_value: int
        """
        if max_value is None:
            self._max_value = None
            self._cur_value = None
        else:
            self.start(max_value)

    def start(self, max_value):
        """
        :param max_value: int
        :return: None
        """
        self._max_value = max_value
        self._cur_value = 0

    def add_progress(self, value=1):
        """
        :param value: int
        :return: ProcessStatus
        """
        self._cur_value += value
        if self._cur_value == self._max_value:
            return ProcessStatus.COMPLETED
        else:
            return ProcessStatus.STARTED


class ProgressBarManager(BaseManager):
    pass
