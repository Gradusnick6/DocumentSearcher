from Model.Message.Message import Message
from Model.Message.MessageType import MessageType
import ViewModel


class MessageList:
    def __init__(self, operating_log_printer):
        """
        :param operating_log_printer: объект занимающийся оперативным выводом новых сообщений
        """
        self.__messages = []
        self.__cur_lvl = 0
        self.__op_log_printer = operating_log_printer

    def add_info_message(self, msg_text):
        """
        Добавляет сообщение в список
        :param msg_text: str. Текст сообщения
        :return: None
        """
        try:
            self.__add_message(MessageType.INF, msg_text)
        except Exception as ex:
            raise ex

    def add_error_message(self, msg_text):
        """
        Добавляет сообщение в список
        :param msg_text: str. Текст сообщения
        :return: None
        """
        try:
            self.__add_message(MessageType.ERR, msg_text)
        except Exception as ex:
            raise ex

    def add_crit_error_message(self, msg_text):
        """
        Добавляет сообщение в список
        :param msg_text: str. Текст сообщения
        :return: None
        """
        try:
            self.__add_message(MessageType.CRT, msg_text)
        except Exception as ex:
            raise ex

    def __add_message(self, msg_type, msg_text):
        """
        Добавляет сообщение в список
        :param msg_type: MessageType
        :param msg_text: str
        :return: None
        """
        try:
            if isinstance(msg_text, str):
                msg = Message(msg_type, msg_text, self.__cur_lvl)
            else:
                msg_text = f"Попытка добавить в журнал не строку. Добавляется {type(msg_text)}"
                msg = Message(MessageType.ERR, msg_text, self.__cur_lvl)
            self.__messages.append(msg)
            self.__op_log_printer.update(msg)
        except Exception as ex:
            raise ex

    def get_message_list(self):
        """
        :return: list<str>
        """
        return self.__messages

    def get_header(self):
        """
        :return: str
        """
        return (f"   Время  | Тип |                               Текст сообщения\n"
                "------------------------------------------------------------------------------------------------------")

    def increment_lvl(self):
        """
        :return: None
        """
        self.__cur_lvl += 1

    def decrement_lvl(self):
        """
        :return: None
        """
        if self.__cur_lvl > 0:
            self.__cur_lvl -= 1

    def set_zero_lvl(self):
        """
        :return: None
        """
        self.__cur_lvl = 0
        