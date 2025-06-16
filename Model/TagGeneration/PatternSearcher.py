import re


class PatternSearcher:
    def __init__(self):
        self.__search_str = []

    def get_search_result(self):
        """
        :return: list<str> Результат исследования
        """
        return self.__search_str

    def search(self, list_text, regex):
        """
        :param list_text: list<str>. Источник поиска
        :param regex: str
        :return: None
        """
        try:
            self.__search_str = []
            for i in range(len(list_text)):
                self.__search_str += re.findall(regex, list_text[i])
        except Exception as ex:
            raise ex

    def add_searched_str_by_slash(self):
        """
        Обрабатывает знак "/" в найденных шаблонах
        :return: None
        """
        try:
            result = []
            for tag in self.__search_str:
                if '/' in tag:
                    result += self.__cut_str_by_slash(tag)
                else:
                    result.append(tag)
            self.__search_str = result
        except Exception as ex:
            raise ex

    def __cut_str_by_slash(self, string):
        try:
            # Разделяем строку на две части: основную и оставшуюся
            main_part, rest = string.split('/', 1)

            # Разделяем оставшуюся часть по символу '/'
            rest_parts = rest.split('/')

            result = [main_part]
            # Создаём список строк, объединяя основную часть с каждой из оставшихся частей
            result += [f"{main_part[0:len(part) * (-1)]}{part}" for part in rest_parts]

            return result
        except Exception as ex:
            raise ex

    def delete_duplicate(self):
        """
        удаляет дубликаты в списке-результате поиска
        :return: None
        """
        data_set = set(self.__search_str)
        self.__search_str = list(data_set)

    def delete_str_without_letter(self):
        """
        Удаляет строки без букв в результате поиска
        :return: None
        """
        try:
            self.__search_str = [match for match in self.__search_str if self.__contains_letter(match)]
        except Exception as ex:
            raise ex

    def delete_str_without_digit(self):
        """
        Удаляет строки без цифр в результате поиска
        :return: None
        """
        try:
            self.__search_str = [match for match in self.__search_str if self.__contains_digit(match)]
        except Exception as ex:
            raise ex

    def __contains_letter(self, s):
        """
        проверка наличия букв в строке s
        :return: bool. True - буквы есть; False - букв нет
        """
        try:
            return any(char.isalpha() for char in s)
        except Exception as ex:
            raise ex

    def __contains_digit(self, s):
        """
        проверка наличия цифр в строке s
        :return: bool. True - цифры есть; False - цифр нет
        """
        try:
            return any(char.isdigit() for char in s)
        except Exception as ex:
            raise ex

    def uppercase(self):
        """
        Перевод букв в результате поиска верхний регистр
        :return: None
        """
        try:
            self.__search_str = [string.upper() for string in self.__search_str]
        except Exception as ex:
            raise ex

    def lowercase(self):
        """
        Перевод букв в результате поиска нижний регистр
        :return: None
        """
        try:
            self.__search_str = [string.lower() for string in self.__search_str]
        except Exception as ex:
            raise ex
