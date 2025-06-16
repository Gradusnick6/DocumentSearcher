from Model.DataFormat.Pattern import Pattern


class PatternList:
    def __init__(self, pattern_list):
        """
        :param pattern_list: list<Pattern>
        """
        self.__patterns = pattern_list

    def __len__(self):
        """
        len(list<Pattern>)
        :return: int
        """
        try:
            return len(self.__patterns)
        except Exception as ex:
            raise ex

    def __iter__(self):
        """
        :return: iter(list<Pattern>)
        """
        try:
            return iter(self.__patterns)
        except Exception as ex:
            raise ex

    def __getitem__(self, key):
        """
        get operator[]
        :param key: int
        :return: Pattern
        """
        try:
            return self.__patterns[key]
        except Exception as ex:
            raise ex

    def add_pattern(self, pattern):
        """
        :param pattern: Pattern
        """
        try:
            self.__patterns.append(pattern)
        except Exception as ex:
            raise ex

    @classmethod
    def from_list(cls, list_data):
        """
        Создание объекта класса по сериализованному списку
        :param list_data: list<Pattern>
        :return: PatternList
        """
        try:
            pattern_list = []
            for pattern in list_data:
                pattern_list.append(Pattern.from_dict(pattern))
            return cls(
                pattern_list=pattern_list
            )
        except Exception as ex:
            raise ex

    def to_list(self):
        """
        Получение сериализованного списка по объекту
        :return: list<Pattern>
        """
        try:
            pattern_list = []
            for pattern in self.__patterns:
                pattern_list.append(pattern.to_dict())
            return pattern_list
        except Exception as ex:
            raise ex

    def get_unique_type_list(self):
        """
        :return: list<PatternType>
        """
        result = set()
        for pattern in self.__patterns:
            result.add(pattern.get_metadata().get_type())
        return list(result)

    def get_unique_name_list(self):
        """
        :return: list<str>
        """
        result = set()
        for pattern in self.__patterns:
            result.add(pattern.get_metadata().get_name())
        return list(result)
