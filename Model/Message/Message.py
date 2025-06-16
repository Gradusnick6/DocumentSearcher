from Model.Service import TimeHandler

from datetime import datetime


class Message:
    def __init__(self, msg_type, msg_text, lvl):
        """
        :param msg_type: MessageType
        :param msg_text: str
        :param lvl: int
        """
        self.type = msg_type
        self.text = msg_text
        self.lvl = lvl
        self.time = datetime.now().time()

    def get_str(self):
        """
        :return: str
        """
        return (f"({TimeHandler.get_str_by_time(self.time)})| "  # время
                f"{self.type.name} | "  # тип 
                f"{self.__get_offset_by_lvl(self.lvl)}{self.text}")  # текст

    def __get_offset_by_lvl(self, lvl):
        return '    ' * lvl
