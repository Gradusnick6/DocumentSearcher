import ViewModel
from Model.Search.FilePatternSearcher import FilePatternSearcher
from Model.DataFormat import (PatternStringList, PatternStringDict,
                              PatternStringSearchResult, SearchResult)
from multiprocessing import Pool
import pandas as pd
import re
import pickle
from openpyxl.utils import get_column_letter


class ExcelPatternSearcher(FilePatternSearcher):
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

            # result_dict = self.__get_searched_tags_by_page(self._file_path, '18',
            #                                                pickle.dumps(self._pattern_string_dict['18']))

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
            xl = pd.ExcelFile(file_path)
            for sheet_name in xl.sheet_names:
                df = xl.parse(sheet_name)  # Чтение листа в DataFrame

                for for_search_string in source_list:  # Поиск каждой строки в DataFrame
                    metainfo = for_search_string.get_metadata()
                    string = for_search_string.get_string()
                    regex = for_search_string.get_regex()

                    # Поиск ячеек, содержащих строку
                    matches = df.map(lambda cell_text: bool(re.search(regex, str(cell_text))))
                    # Получение индексов ячеек, где найдено совпадение
                    matching_cells = matches.stack()[matches.stack()].index.tolist()

                    search_result_list = []
                    if matching_cells:  # Добавление результатов в список
                        for row, col in matching_cells:
                            col_index = df.columns.get_loc(col)  # Преобразование индекса столбца в число
                            col_letter = get_column_letter(col_index + 1)  # Преобразование индекса столбца в букву
                            cell_address = f"{col_letter}{row + 2}"
                            search_result_list.append(SearchResult(file_name, sheet_name, cell_address))

                    if string not in searched_dict:  # Добавление элемент PatternStringSearchResult в промежуточный словарь
                        searched_dict[string] = PatternStringSearchResult(string, metainfo, regex)
                    searched_dict[string].add_search_result(search_result_list)

            searched_pslist = PatternStringList()  # Конвертация данных промежуточного словаря в возвращаемый тип
            for key, value in searched_dict.items():
                searched_pslist.add_value(value)
            return searched_pslist
        except Exception as ex:
            raise ex
