class SearchedTextManager:
    def __init__(self, text):
        """
        :param text: list<str>
        """
        self.__text = text
        self.__clear_of_typos()

    def clear_of_verified(self, list_str):
        """
        Очищает текст от строк
        :param list_str: list<str>
        :return: None
        """
        try:
            for i in range(len(self.__text)):
                for string in list_str:
                    if isinstance(string, tuple):
                        full_match = ''
                        for part in string:  # проходим по кортежу
                            full_match = ''.join(part)  # Объединяем части совпадения
                        self.__text[i] = self.__text[i].replace(full_match, '')
                    else:
                        self.__text[i] = self.__text[i].replace(string, '')
        except Exception as ex:
            raise ex

    def get_text(self):
        """
        :return: list<str>
        """
        return self.__text

    def __clear_of_typos(self):
        """
        Удаление дефектов в тексте для удобного анализа
        :return: None
        """
        try:
            self.__text = self.__get_list_str_without_all_excess_space(self.__text)
        except Exception as ex:
            raise ex

    def __get_list_str_without_all_excess_space(self, list_text):
        """
        Удаление лишних пробелов в списке строк
        :param list_text: list<str>
        :return: list<str>
        """
        try:
            for i in range(len(list_text)):
                list_text[i] = self.__get_str_without_all_excess_space(list_text[i])
            return list_text
        except Exception as ex:
            raise ex

    def __get_str_without_all_excess_space(self, checked_str):
        """
        Удаление лишних пробелов в строке
        :param checked_str: str
        :return: str
        """
        try:
            checked_str = checked_str.replace('\n', '')
            checked_str = checked_str.replace('\t', '')
            checked_str = checked_str.replace('- ', '-')
            checked_str = checked_str.replace(' -', '-')
            checked_str = checked_str.replace('_ ', '_')
            checked_str = checked_str.replace(' _', '_')
            checked_str = checked_str.replace('/ ', '/')
            checked_str = checked_str.replace(' /', '/')
            return checked_str
        except Exception as ex:
            raise ex
