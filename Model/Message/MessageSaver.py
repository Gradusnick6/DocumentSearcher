from Model.Service import TimeHandler


class MessageSaver:
    def __init__(self):
        self.__file_path = self.__generate_file_path()

    def __generate_file_path(self):
        self.__part_filepath = "logs/ds"
        self.__fileex = ".log"
        cur_datetime = TimeHandler.get_cur_datetime_str()
        cur_datetime = cur_datetime.replace(":", "-")
        return f"{self.__part_filepath}_{cur_datetime}{self.__fileex}"

    def get_file_path(self):
        """
        :return: str
        """
        return self.__file_path

    def save_to_file(self, message_list):
        """
        :param message_list: Message_List
        :return: str. Возвращает относительный путь к файлу, в который записаны логи
        """
        try:
            log_data = self.__convert_for_write(message_list)
            with open(self.__file_path, 'w') as file:
                file.write(log_data)
            return self.__file_path
        except Exception as ex:
            raise ex

    def __convert_for_write(self, message_list):
        """
        :param message_list: Message_List
        :return: str
        """
        messages = message_list.get_message_list()
        messages_list = [m.get_str() for m in messages]
        log_data_list = [message_list.get_header()] + messages_list
        separator = "\n"
        log_data_str = separator.join(log_data_list)
        return log_data_str
