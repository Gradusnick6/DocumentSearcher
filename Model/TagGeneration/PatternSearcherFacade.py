from Model.TagGeneration.PdfReader import PdfReader
from Model.TagGeneration.SearchedTextManager import SearchedTextManager
from Model.TagGeneration.PatternSearcher import PatternSearcher
from Model.DataFormat import PatternStringList, PatternString, PatternStringDict

import ViewModel


class PatternSearcherFacade:
    @staticmethod
    def get_pattern_string_from_file(file_path, patterns):
        """
        :param file_path: str
        :param patterns: PatternList
        :return: PatternStringDict
        """
        try:
            pdf_reader = PdfReader(file_path)
            page_count = pdf_reader.get_page_count()
            ViewModel.message_list.add_info_message(f"Открыт файл {file_path}. Всего страниц - {page_count}")
            ViewModel.multi_progress_bar.start_next_process(page_count)

            document_data = PatternStringDict()
            for page_index in range(page_count):
                ViewModel.multi_progress_bar.add_progress()
                list_text = pdf_reader.get_text_by_ipage(page_index)
                data_from_list = PatternSearcherFacade.get_pattern_strings_from_text(list_text, patterns)
                document_data.add_value(str(page_index + 1), data_from_list)
            return document_data
        except Exception as ex:
            raise ex

    @staticmethod
    def get_pattern_strings_from_text(text, patterns):
        """
        :param text: list<str>
        :param patterns: PatternList
        :return: PatternStringList
        """
        try:
            text_manager = SearchedTextManager(text)
            pattern_string_list = PatternStringList()
            for pattern in patterns:
                buf = PatternSearcherFacade.__get_pattern_strings_from_text_by_pattern(text_manager, pattern)
                pattern_string_list += buf
            return pattern_string_list
        except Exception as ex:
            raise ex

    @staticmethod
    def __get_pattern_strings_from_text_by_pattern(text_manager, pattern):
        """
        :param text_manager: SearchedTextManager
        :param pattern: Pattern
        :return: PatternStringList
        """
        try:
            searcher = PatternSearcher()
            searcher.search(text_manager.get_text(), pattern.get_regex(0))
            text_manager.clear_of_verified(searcher.get_search_result())

            if pattern.is_del_without_letter():
                searcher.delete_str_without_letter()
            if pattern.is_del_without_digit():
                searcher.delete_str_without_digit()
            searcher.add_searched_str_by_slash()
            searcher.delete_duplicate()

            str_list = searcher.get_search_result()
            pattern_strs = [PatternString(string, pattern.get_metadata()) for string in str_list]
            pattern_string_list = PatternStringList(pattern_strs)
            return pattern_string_list
        except Exception as ex:
            raise ex
