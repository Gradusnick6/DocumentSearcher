class SearchResult:
    def __init__(self, file_name, sheet, location=""):
        """
        :param file_name: str
        :param sheet: str
        :param location: str
        """
        self.__file_name = file_name
        self.__sheet = sheet
        self.__location = location

    def get_location(self):
        """
        :return: str
        """
        try:
            return f"{self.__location}"
        except Exception as ex:
            raise ex

    def get_file_name(self):
        """
        :return: str
        """
        return self.__file_name

    def get_sheet(self):
        """
        :return: str
        """
        return self.__sheet

    def get_group_name(self):
        """
        :return: str
        """
        try:
            if self.get_sheet() != "":
                return f"{self.get_file_name()}_{self.get_sheet()}"
            else:
                return f"__{self.get_file_name()}__"
        except Exception as ex:
            raise ex
