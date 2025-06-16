from abc import ABC, abstractmethod


class FilePatternSearcher(ABC):
    def __init__(self, file_path, pattern_string_dict):
        """
        :param file_path: str
        :param pattern_string_dict: PatternStringDict<string, PatternStringList>
        """
        self._file_path = file_path
        self._pattern_string_dict = pattern_string_dict

    @abstractmethod
    def search(self):
        pass
