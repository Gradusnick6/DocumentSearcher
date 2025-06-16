from Model.DataFormat.PatternStringContainer import PatternStringContainer
from Model.DataFormat.SortType import SortType


class PatternStringDict(PatternStringContainer):
    def __init__(self, pattern_string_container=None):
        """
        :param pattern_string_container: dict<string, PatternStringContainer>
        """
        super().__init__()
        if pattern_string_container is None:
            pattern_string_container = {}
        self._value = pattern_string_container  # dict<string, PatternStringContainer>

    def __add__(self, other):
        """
        operator+
        :param other: PatternStringDict
        :return: PatternStringDict
        """
        if isinstance(other, PatternStringDict):
            sum_value = {}  # для суммирования значений совпадающих ключей
            for key, value in self.items():
                if key in other.keys():
                    sum_value[key] = self[key] + other[key]
            new_value = self.get_value() | other.get_value()
            return PatternStringDict(new_value | sum_value)
        return NotImplemented

    def __iter__(self):
        """
        :return: iter(dict<PatternStringList>.items())
        """
        try:
            return iter(self._value.items())
        except Exception as ex:
            raise ex

    def items(self):
        """
        Возвращает (keys, values)
        :return: tuple(list<str>, PatternStringList)
        """
        try:
            return self._value.items()
        except Exception as ex:
            raise ex

    def keys(self):
        """
        :return: list<str>
        """
        try:
            return self._value.keys()
        except Exception as ex:
            raise ex

    def add_value(self, key, pattern_string_container):
        """
        Исключения: TypeError()
        :param key: str
        :param pattern_string_container: PatternStringContainer
        :return: None
        """
        if not isinstance(pattern_string_container, PatternStringContainer):
            raise TypeError()
        if not isinstance(key, str):
            raise TypeError()

        try:
            if key in self._value:
                self._value[key] += pattern_string_container
            else:
                self._value[key] = pattern_string_container
        except Exception as ex:
            raise ex

    def upgrade_item_type(self, arg_box):
        """
        Изменяет тип элемента контейнера нижнего уровня
        Исключения: TypeError()
        :param arg_box: UpgradeArgumentBox
        :return: None
        """
        try:
            for key in self._value.keys():
                self._value[key].upgrade_item_type(arg_box)
        except Exception as ex:
            raise ex

    def sort(self, sort_type, reverse=False):
        """
        :param sort_type: SortType.BY_PATTERN_TYPE; SortType.BY_PATTERN_TYPE; SortType.BY_STRING; SortType.BY_DICT_KEY
        :param reverse: bool
        :return: None
        """
        try:
            if (sort_type == SortType.BY_STRING or
                    sort_type == SortType.BY_PATTERN_TYPE or
                    sort_type == SortType.BY_PATTERN_NAME):
                self.__sort_container(sort_type, reverse)
            elif sort_type == SortType.BY_DICT_KEY:
                self.__sort_by_key(reverse)
            else:
                raise TypeError()
        except Exception as ex:
            raise ex

    def __sort_container(self, sort_type, reverse):
        """
        Вызывает функции сортировки значений словаря
        :param reverse: bool - Флаг для обратной сортировки
        :return: None
        """
        try:
            for key in self._value.keys():
                self._value[key].sort(sort_type, reverse)
        except Exception as ex:
            raise ex

    def __sort_by_key(self, reverse):
        """
        Сортирует словарь по ключу
        :param reverse: bool - Флаг для обратной сортировки
        :return: None
        """
        try:
            sorted_items = sorted(self._value.items(),
                                  key=lambda item: item[0],
                                  reverse=reverse)
            self._value = dict(sorted_items)
        except Exception as ex:
            raise ex
