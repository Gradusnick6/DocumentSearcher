class SupportedFileExtension:
    @staticmethod
    def get_source_extensions():
        """
        :return: list<str>
        """
        return ["pdf"]

    @staticmethod
    def get_excel_for_search_extensions():
        """
        :return: list<str>
        """
        return ["xlsm"]

    @staticmethod
    def get_pdf_for_search_extensions():
        """
        :return: list<str>
        """
        return ["pdf"]

    @staticmethod
    def get_for_search_extensions():
        """
        :return: list<str>
        """
        return (SupportedFileExtension.get_pdf_for_search_extensions() +
                SupportedFileExtension.get_excel_for_search_extensions())
