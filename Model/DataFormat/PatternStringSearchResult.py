from Model.DataFormat.PatternString import PatternString


class PatternStringSearchResult(PatternString):
    def __init__(self, string=None, metadata=None, regex=None, arg_box=None):
        """
        Заполнять либо только string, metadata и pattern_str либо только arg_box
        Исключения: TypeError, ValueError
        :param string: str
        :param metadata: PatternMetaData
        :param regex: str
        :param arg_box: не используется
        """
        try:
            super().__init__(string, metadata, arg_box)
            if isinstance(regex, str):
                self.__regex = regex
            else:
                raise TypeError
            self.__search_results = []  # list<SearchResult>
            self.__group_names = None  # list<str>
        except Exception as ex:
            raise ex

    def __add__(self, other):
        """
        operator+
        :param other:
        :return:
        """
        if isinstance(other, PatternStringSearchResult):
            sr1 = self.get_search_result()
            sr2 = other.get_search_result()
            new_ps = PatternStringSearchResult(self.get_string(), self.get_metadata(), self.__regex)
            new_ps.add_search_result(sr1)
            new_ps.add_search_result(sr2)
            return new_ps
        return NotImplemented

    def get_search_result(self):
        """
        :return: # list<SearchResult>
        """
        return self.__search_results

    def add_search_result(self, result_list):
        """
        :param result_list: list<SearchResult>
        """
        try:
            self.__search_results += result_list
        except Exception as ex:
            raise ex

    def get_param_list(self, group_name=None):
        """
        :type group_name: str
        :return: list
        """
        try:
            if group_name is not None:
                required_locations = [result for result in self.__search_results if result.get_group_name() == group_name]
            else:
                required_locations = self.__search_results

            search_result_list = [result.get_location() for result in required_locations]
            return self._metadata.get_metainfo_list() + [self.__regex] + [self._string] + search_result_list
        except Exception as ex:
            raise ex

    def calculate_unique_group_names(self):
        """
        :return: None
        """
        try:
            file_page_list = []
            for search_result in self.__search_results:
                file_page_list.append(search_result.get_group_name())
            file_page_set = set(file_page_list)
            self.__group_names = list(file_page_set)
        except Exception as ex:
            raise ex

    def get_unique_group_names(self):
        """
        :return: list<str>
        """
        return self.__group_names

    def is_empty_searched_result(self):
        """
        :return: bool
        """
        try:
            return len(self.__search_results) == 0
        except Exception as ex:
            raise ex
