from Model.Service.ProgressBar.ProcessStatus import ProcessStatus


class MultiProcessProgressBar:
    def __init__(self, progress_bar_list, process_names, message_storage):
        """
        :param progress_bar_list: list<ProgressBar>
        :param process_names: list<str>
        :param message_storage: Message_List
        """
        if isinstance(progress_bar_list, list):
            self.__process_names = process_names
            self.__progress_bar_list = progress_bar_list
            self.__process_count = len(progress_bar_list)

            self.__num_cur_process = -1
            self.__cur_proc_state = ProcessStatus.NOT_STARTED
        else:
            raise TypeError()
        self.__message_storage = message_storage

    def get_num_cur_process(self):
        """
        :return: int
        """
        return self.__num_cur_process

    def get_process_count(self):
        """
        :return: int
        """
        return self.__process_count

    def start_next_process(self, max_value=None):
        try:
            if self.__num_cur_process == self.__process_count - 1:
                raise Exception("Ошибка Мульти прогресс бара. Попытка приступить к несуществующему процессу")
            self.__num_cur_process += 1
            process_name = self.__process_names[self.__num_cur_process]

            selecting_str = "---------------------------"

            self.__message_storage.add_info_message(f"{selecting_str} Процесс {self.__get_progress_str()} {selecting_str}")
            self.__message_storage.add_info_message(f"Начали {process_name} ")
            if max_value is not None:
                cur_progress_bar = self.__progress_bar_list[self.__num_cur_process]
                cur_progress_bar.start(max_value)
            self.__cur_proc_state = ProcessStatus.STARTED
        except Exception as ex:
            raise ex

    def add_progress(self, value=1):
        try:
            if self.__cur_proc_state == ProcessStatus.NOT_STARTED:
                raise Exception(f"Попытка обновить прогресс в не начатом процессе в MultiProcessProgressBar. "
                                f"Текущий процесс {str(self.__num_cur_process)}")
            elif self.__cur_proc_state == ProcessStatus.STARTED:
                cur_progress_bar = self.__progress_bar_list[self.__num_cur_process]
                self.__cur_proc_state = cur_progress_bar.add_progress(value)

            if self.__cur_proc_state == ProcessStatus.COMPLETED:
                process_name = self.__process_names[self.__num_cur_process]
                self.__message_storage.add_info_message(f"Завершен процесс {self.__get_progress_str()}. "
                                                        f"Завершили {process_name}")
            elif (self.__cur_proc_state != ProcessStatus.STARTED and
                  self.__cur_proc_state != ProcessStatus.NOT_STARTED):
                raise ValueError(f"{self.__cur_proc_state.name}. Статус не обрабатывается MultiProcessProgressBar")
        except Exception as ex:
            raise ex

    def __get_progress_str(self):
        """
        :return: str
        """
        return f"{str(self.__num_cur_process + 1)}/{str(self.__process_count)}"
