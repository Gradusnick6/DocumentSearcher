import platform


class HandlerByOS:
    def __init__(self):
        self.os_name = platform.system()

    def get_file_path(self, file_path):
        """
        :return: str. file_path отформатированный согласно используемой OS
        """
        try:
            if self.__is_windows():
                return file_path.replace("/", "\\")
            return file_path
        except Exception as ex:
            raise ex
        # TODO: сделать для линукс

    def __is_windows(self):
        return self.os_name == "Windows"

    def __is_linux(self):
        return self.os_name == "Linux"

    def __is_mac(self):
        return self.os_name == "Darwin"


handler_by_os = HandlerByOS()
