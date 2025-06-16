import ViewModel
from Model.Search.FilePatternSearcher import FilePatternSearcher
from Model.DataFormat import (PatternStringList, PatternStringDict,
                              PatternStringSearchResult, SearchResult)
from Model.TagGeneration import PdfReader, PatternSearcher, SearchedTextManager

from multiprocessing import Pool
import pickle


class PdfPatternSearcher(FilePatternSearcher):
    def __init__(self, file_path, pattern_string_dict):
        """
        :param file_path: str
        :param pattern_string_dict: PatternStringDict<string, PatternStringList<PatternStringForSearch>>
        """
        super().__init__(file_path, pattern_string_dict)

    def search(self):
        """
               :return: PatternStringDict<string, PatternStringList<PatternStringSearchResult>>
               """
        try:
            keys_list = list(self._pattern_string_dict.keys())

            args_list = [(self._file_path, key,
                          pickle.dumps(self._pattern_string_dict[key]),
                          pickle.dumps(ViewModel.multi_progress_bar))
                         for key in keys_list]

            # result_dict = self.get_searched_tags_by_page(self._file_path, '3',
            #                                                pickle.dumps(self._pattern_string_dict['3']),
            #                                             pickle.dumps(ViewModel.multi_progress_bar))


            with Pool() as pool:
                # result_list = list<PatternStringDict<string, PatternStringList<PatternStringSearchResult>>>
                result_list = pool.starmap(self.get_searched_tags_by_page, args_list)
            result_dict = PatternStringDict()
            for result in result_list:
                result_dict += result
            return result_dict
        except Exception as ex:
            raise ex

    def get_searched_tags_by_page(self, file_path, key, ser_pattern_for_search_pslist, ser_multi_progress_bar):
        """
        :param file_path: str
        :param key: str
        :param ser_pattern_for_search_pslist: pickle PatternStringList<PatternStringForSearch>
        :param ser_multi_progress_bar: pickle MultiProcessProgressBar
        :return: PatternStringDict<string, PatternStringList<PatternStringSearchResult>>
        """
        try:
            pattern_for_search_list = pickle.loads(ser_pattern_for_search_pslist)
            search_result_pslist = self.__get_pslist_matches(file_path, pattern_for_search_list)

            search_result_psdict = PatternStringDict()
            search_result_psdict.add_value(key, search_result_pslist)

            multi_progress_bar = pickle.loads(ser_multi_progress_bar)
            multi_progress_bar.add_progress()
            return search_result_psdict
        except Exception as ex:
            raise ex

    def __get_pslist_matches(self, file_path, source_list):
        """
        :param file_path: str
        :param source_list: PatternStringList<PatternStringForSearch>
        :return: PatternStringList<PatternStringSearchResult>
        """
        try:
            file_name = file_path.split("\\")[-1]
            file_name = file_name.split(".")[0]
            searched_dict = {}
            pdf = PdfReader(file_path)
            for page_index in range(pdf.get_page_count()):
                page_text = pdf.get_text_by_ipage(page_index)
                text_manager = SearchedTextManager(page_text)

                for for_search_string in source_list:  # Поиск каждой строки в page_text
                    metainfo = for_search_string.get_metadata()
                    string = for_search_string.get_string()
                    regex = for_search_string.get_regex()

                    searcher = PatternSearcher()
                    searcher.search(text_manager.get_text(), regex)
                    searcher.add_searched_str_by_slash()
                    searcher.delete_duplicate()
                    str_list = searcher.get_search_result()

                    search_result_list = []
                    if len(str_list) > 0:  # Добавление результатов в список
                        search_result_list.append(SearchResult(file_name, "", "page " + str(page_index + 1)))
                    if string not in searched_dict:
                        searched_dict[string] = PatternStringSearchResult(string, metainfo, regex)
                    searched_dict[string].add_search_result(search_result_list)

            searched_pslist = PatternStringList()  # Конвертация данных промежуточного словаря в возвращаемый тип
            for key, value in searched_dict.items():
                searched_pslist.add_value(value)
            return searched_pslist
        except Exception as ex:
            raise ex
