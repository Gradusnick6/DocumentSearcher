from Model.DirectoryWork.SupportedFileExtension import SupportedFileExtension
from Model.Search.SearcherKind import SearcherKind
from Model.Search.PdfPatternSearcher import PdfPatternSearcher
from Model.Search.ExcelPatternSearcher import ExcelPatternSearcher


class PatternStringSearcherByFile:
    def __init__(self, file_path, pattern_string_dict):
        """
        :param file_path: str
        :param pattern_string_dict: PatternStringDict<string, PatternStringList>
        """
        self.__file_path = file_path
        self.__pattern_string_dict = pattern_string_dict

    def search(self):
        """
        :return: PatternStringDict<string, PatternStringDict<string, PatternStringList>>
        """
        try:
            searcher = self.__get_searcher()
            return searcher.search()
        except Exception as ex:
            raise ex

    def __get_searcher(self):
        """
        :return: FilePatternSearcher
        """
        try:
            searcher_kind = self.__get_searcher_kind()
        except TypeError as ex:
            raise ex
        if searcher_kind == SearcherKind.EXCEL_SEARCHER:
            return ExcelPatternSearcher(self.__file_path, self.__pattern_string_dict)
        elif searcher_kind == SearcherKind.PDF_SEARCHER:
            return PdfPatternSearcher(self.__file_path, self.__pattern_string_dict)

    def __get_searcher_kind(self):
        """
        Возвращает вид серчера по типу файла
        Исключения TypeError
        :return: SearcherKind
        """
        ext = self.__file_path.split('.')[-1]
        if ext in SupportedFileExtension.get_excel_for_search_extensions():
            return SearcherKind.EXCEL_SEARCHER
        elif ext in SupportedFileExtension.get_for_search_extensions():
            return SearcherKind.PDF_SEARCHER
        else:
            raise TypeError()
