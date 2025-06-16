from enum import Enum


class SortType(Enum):
    BY_STRING = 2,  # по строке
    BY_PATTERN_TYPE = 3,  # по типу паттерна
    BY_PATTERN_NAME = 4,  # по имени паттерна
    BY_DICT_KEY = 5  # по ключу словаря
