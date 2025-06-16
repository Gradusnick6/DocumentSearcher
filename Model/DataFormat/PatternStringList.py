from Model.DataFormat.PatternStringContainer import PatternStringContainer
from Model.DataFormat.PatternString import PatternString
from Model.DataFormat.SortType import SortType
from Model.DataFormat.UpgradeArgumentBox import UpgradeArgumentBox


class PatternStringList(PatternStringContainer):
    def __init__(self, pattern_strings=None):
        """
        :param pattern_strings: list<PatternString>
        """
        super().__init__()
        if pattern_strings is None:
            pattern_strings = []
        self._value = pattern_strings

    def __add__(self, other):
        """
        operator+
        :param other: PatternStringList
        :return: PatternStringList
        """
        if isinstance(other, PatternStringList):
            new_list = []
            for value_s in self:
                is_find = False
                for value_o in other:
                    if value_o.get_string() == value_s.get_string():
                        new_list.append(value_s + value_o)
                        is_find = True
                        break
                if not is_find:
                    new_list.append(value_s)

            for value_o in other:
                is_find = False
                for value_s in self:
                    if value_o.get_string() == value_s.get_string():
                        is_find = True
                        break
                if not is_find:
                    new_list.append(value_o)
            return PatternStringList(new_list)
        return NotImplemented

    def __iter__(self):
        """
        :return: iter(list<PatternString>)
        """
        try:
            return iter(self._value)
        except Exception as ex:
            raise ex

    def add_value(self, pattern_string):
        """
        Исключения: TypeError()
        :param pattern_string: PatternString
        :return: None
        """
        if isinstance(pattern_string, PatternString):
            self._value.append(pattern_string)
        else:
            raise TypeError()

    def upgrade_item_type(self, arg_box):
        """
        Изменяет тип элемента контейнера
        Исключения: TypeError()
        :param arg_box: UpgradeArgumentBox
        :return: None
        """
        try:
            item_type = arg_box.obj
            for i in range(len(self._value)):
                upgrade_box = UpgradeArgumentBox(self._value[i], arg_box.args)
                self._value[i] = item_type(arg_box=upgrade_box)
        except Exception as ex:
            raise ex

    def sort(self, sort_type, reverse=False):
        """
        Исключения: TypeError()
        :param sort_type: SortType.BY_PATTERN_TYPE; SortType.BY_PATTERN_TYPE; SortType.BY_STRING
        :param reverse: bool
        :return: None
        """
        try:
            if sort_type == SortType.BY_PATTERN_NAME:
                self.__sort_by_pattern_name(reverse)
            elif sort_type == SortType.BY_PATTERN_TYPE:
                self.__sort_by_pattern_type(reverse)
            elif sort_type == SortType.BY_STRING:
                self.__sort_by_string(reverse)
            else:
                raise TypeError()
        except Exception as ex:
            raise ex

    def __sort_by_pattern_name(self, reverse=False):
        """
        Сортирует список PatternString по имени паттерна.
        :param reverse: bool - Флаг для обратной сортировки
        :return: None
        """
        try:
            self._value = sorted(
                self._value,
                key=lambda x: x.get_metadata().get_name(),
                reverse=reverse
            )
        except Exception as ex:
            raise ex

    def __sort_by_pattern_type(self, reverse=False):
        """
        Сортирует список PatternString по типу паттерна.
        :param reverse: bool - Флаг для обратной сортировки
        :return: None
        """
        try:
            self._value = sorted(
                self._value,
                key=lambda x: x.get_metadata().get_type().value,
                reverse=reverse
            )
        except Exception as ex:
            raise ex

    def __sort_by_string(self, reverse=False):
        """
        Сортирует список PatternString по строке в алфавитном порядке.
        :param reverse: bool - Флаг для обратной сортировки
        :return: None
        """
        try:
            self._value = sorted(
                self._value,
                key=lambda x: x.get_string(),
                reverse=reverse
            )
        except Exception as ex:
            raise ex
