from Model.DataFormat import PatternStringDict
from Model.Search.PatternStringSearcherByFile import PatternStringSearcherByFile
import ViewModel

import ViewModel


class PatternStringSearcher:
    def __init__(self, file_path_list, pattern_string_dict):
        """
        :param file_path_list: list<str>
        :param pattern_string_dict: PatternStringDict<string, PatternStringList>
        """
        self.__file_path_list = file_path_list
        self.__pattern_string_dict = pattern_string_dict

    def search(self):
        """
        :return: PatternStringDict<string, PatternStringDict<string, PatternStringList>>
        """
        try:
            data_psdict = PatternStringDict()
            for file_path in self.__file_path_list:
                searcher_by_file = PatternStringSearcherByFile(file_path, self.__pattern_string_dict)

                ViewModel.multi_progress_bar.start_next_process(len(self.__pattern_string_dict))
                data_psdict += searcher_by_file.search()

            return data_psdict
        except Exception as ex:
            raise ex
