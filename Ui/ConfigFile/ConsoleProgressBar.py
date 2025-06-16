from Model.Service.ProgressBar import ProgressBar
from multiprocessing.managers import BaseManager
from Model.Service.ProgressBar.ProcessStatus import ProcessStatus


class ConsoleProgressBar(ProgressBar):
    def __init__(self, message_storage, max_value=None, segments_count=None):
        """
        :param max_value: int
        :param segments_count: int
        :param message_storage: Message_List

        """
        try:
            super().__init__(max_value)
            if max_value is None:
                self.__next_segment = None
                self.__info_segments = None
                self.__segments_count = None
            else:
                self.start(max_value, segments_count)
            self.__message_storage = message_storage
        except Exception as ex:
            raise ex

    def start(self, max_value, segments_count=5):
        """
        :param max_value: int
        :param segments_count: int
        :return: None
        """
        try:
            super().start(max_value)
            self.__segments_count = segments_count
            segment_offset = max_value / segments_count
            self.__info_segments = [int(segment_offset * i) for i in range(1, self.__segments_count + 1)]
            self.__next_segment = 0
            self.__message_storage.increment_lvl()
        except Exception as ex:
            raise ex

    def add_progress(self, value=1):
        """
        :param value: int
        :return: ProcessStatus
        """
        try:
            # print(f"{self._cur_value}/{self._max_value}  ")
            process_status = super().add_progress(value)
            if self.__info_segments[self.__next_segment] == self._cur_value:
                self.__next_segment += 1
                percent = int(self.__next_segment / self.__segments_count * 100)
                self.__message_storage.add_info_message(f"Завершено на {percent}%")
            if process_status == ProcessStatus.COMPLETED:
                self.__message_storage.decrement_lvl()
            return process_status
        except Exception as ex:
            raise ex


class ConsoleProgressBarManager(BaseManager):
    pass
