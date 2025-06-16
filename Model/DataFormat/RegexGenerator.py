import re
import ViewModel


class RegexGenerator:
    def __init__(self):
        self.__start_letter = "<sP>"
        self.__end_letter = "<eP>"

    def create_regex(self, string, regex):
        """
        Конструирует регулярное выражение на основе строки и regex со специальными литерами
        Если строка и regex не соотносятся либо неправильно сформулирован regex, возвращет искомую строку
        :param string: str.
        :param regex: str.
        :return: str. regex
        """
        try:
            if self.__check_count_letters(regex) and self.__check_alternating_letters(regex):
                new_regex = self.__assemble_regex(string, regex)
                return new_regex
            else:
                return string
        except Exception as ex:
            ViewModel.message_list.add_error_message(f"{string}. {ex.args[0]}")
            raise Exception("", "")

    def __check_count_letters(self, s):
        """
        Проверка совпадения количеств начальных и концевых литер
        Исключения: ValueError
        :param s: str. строка с литерами
        :return: True
        """
        try:
            count_start_letter = s.count(self.__start_letter)
            count_end_letter = s.count(self.__end_letter)

            if count_start_letter != count_end_letter:
                raise ValueError("Не верно сформулирован паттерн. Разное количество краевых литер")
            if count_start_letter == 0:
                return False
            return True
        except Exception as ex:
            raise ex

    def __check_alternating_letters(self, s):
        """
        Проверяет правильность порядка литер (start, end, start,...)
        Исключения: ValueError
        :param s: str. строка с литерами
        :return: True
        """
        try:
            icur = 0
            while True:
                index0 = s.find(self.__start_letter, icur)
                index1 = s.find(self.__end_letter, icur)
                if index0 == - 1 or index1 == - 1:
                    break
                if index0 >= index1:
                    raise ValueError("Не верно сформулирован паттерн. Не верный порядок краевых литер")
                icur = index1 + len(self.__end_letter)
            return True
        except Exception as ex:
            raise ex

    def __assemble_regex(self, string, regex):
        """
        Собирает паттерн, на основе литер
        :param string: str
        :param regex: str
        :return: str
        """
        try:
            iprev = 0
            new_regex = ""
            while True:
                icur = regex.find(self.__start_letter, iprev)
                if icur == -1:
                    new_regex += string
                    break
                # получение строки по регулярному выражению
                iprev, string, new_regex = self.__handle_letter(iprev, icur, string, regex, new_regex, self.__start_letter)
                icur = regex.find(self.__end_letter, iprev)
                # получение регулярного выражения
                iprev, string, new_regex = self.__handle_letter(iprev, icur, string, regex, new_regex, self.__end_letter)
            return new_regex
        except Exception as ex:
            raise ex

    def __handle_letter(self, istart, iend, string, regex, new_regex, litter):
        """
        Производит обработку входящей литеры
        :param istart: int. индекс первого символа попадающего под обработку
        :param iend: int. индекс последнего символа уже не попадающего под обработку
        :param string: str. исходная строка
        :param regex: str. исходный regex
        :param new_regex: str. промежуточное значение нового regex
        :param litter: str. входящая литера
        :return: (int - первый символ попадающий под обработку следующей литеры,
                  str - промежуточное состояние исходной строки,
                  str - промежуточное состояние исходного regex)
        """
        try:
            buf_pattern = regex[istart:iend]
            searched_str = re.search(buf_pattern, string).group()
            str_for_pattern = searched_str if litter == self.__start_letter else buf_pattern
            new_regex += str_for_pattern
            string = string.replace(searched_str, '', 1)
            istart = iend + len(litter)
            return istart, string, new_regex
        except Exception as ex:
            raise ex
