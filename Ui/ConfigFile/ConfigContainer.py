from Model.DataFormat.PatternList import PatternList


class ConfigContainer:
    def __init__(self, source_file, pattern_list, search_files, result_file, is_search):
        """
        :param source_file: str
        :param pattern_list: PatternList
        :param search_files: list<str>
        :param result_file: str
        :param is_search: bool
        """
        self.source_file = source_file
        self.pattern_list = pattern_list
        self.search_files = search_files
        self.result_file = result_file
        self.is_search = is_search

    @classmethod
    def from_dict(cls, dict_data):
        try:
            return cls(
                source_file=dict_data["source_file"],
                pattern_list=PatternList.from_list(dict_data["pattern_list"]),
                search_files=dict_data["search_files"],
                result_file=dict_data["result_file"],
                is_search=dict_data["is_search"]
            )
        except Exception as ex:
            raise ex

    def to_dict(self):
        return {
            "source_file": self.source_file,
            "pattern_list": self.pattern_list.to_list(),
            "search_files": self.search_files,
            "result_file": self.result_file,
            "is_search": self.is_search
        }
