from abc import ABC, abstractmethod


class PatternStringContainer(ABC):
    def __init__(self):
        self._value = None

    @abstractmethod
    def __add__(self, other):
        """
        operator+
        :param other: PatternStringContainer
        :return: PatternStringContainer
        """
        pass

    def __getitem__(self, key):
        return self._value[key]

    def __setitem__(self, key, value):
        try:
            self._value[key] = value
        except Exception as ex:
            raise ex

    def __len__(self):
        try:
            return len(self._value)
        except Exception as ex:
            raise ex

    def get_value(self):
        return self._value

    @abstractmethod
    def upgrade_item_type(self, arg_box):
        """
        Изменяет тип элемента контейнера
        :param arg_box: UpgradeArgumentBox
        :return: None
        """
        pass

    @abstractmethod
    def sort(self, sort_type, reverse=False):
        """
        :param sort_type: SortType
        :param reverse: bool
        :return: None
        """
        pass
