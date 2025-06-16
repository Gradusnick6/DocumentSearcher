from Model.Service import Observer, TimeHandler


class ConsoleLogs(Observer):

    def update(self, msg):
        """
        :param msg: Message
        :return: None
        """
        self.print_message(msg)

    def print_message(self, msg):
        """
        :param msg: Message
        :return: None
        """
        print(msg.get_str())

    def print_header(self, header_str):
        """
        :return: None
        """
        print(f"\n                                           Журнал сообщений")
        print(f"______________________________________________________________________________________________________")
        print(header_str)
