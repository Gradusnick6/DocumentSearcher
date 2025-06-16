import fitz  # PyMuPDF
import re


class PdfReader:
    def __init__(self, file_path):
        """
        :param file_path: str
        """
        try:
            self.__document = fitz.open(file_path)
        except Exception as ex:
            raise ex

    def get_text_by_ipage(self, page_i):
        """
        :param page_i: int. Индекс страницы в документе
        :return: list<str>
        """
        try:
            xhtml_text = self.__get_page_str(page_i)
            return self.__get_list_str_by_xhtml(xhtml_text)
        except Exception as ex:
            raise ex

    def get_page_count(self):
        """
        :return: int
        """
        return len(self.__document)

    def __get_page_str(self, page_index):
        """
        :param page_index: int. Индекс страницы в документе
        :return: list<str> Возвращает текст со страницы в формате xhtml
        """
        try:
            page = self.__document.load_page(page_index)
            page_text = page.get_text("xhtml")
            return page_text
        except Exception as ex:
            raise ex

    def __get_list_str_by_xhtml(self, xhtml_string):
        """
        :param xhtml_string: преобразуем список строк в формате xhtml в список обычных строк
        :return: list<str>
        """
        try:
            # Используем регулярное выражение для извлечения текста между тегами <p> и </p>
            pattern = r"<p>(.*?)</p>"
            return re.findall(pattern, xhtml_string)
        except Exception as ex:
            raise ex
