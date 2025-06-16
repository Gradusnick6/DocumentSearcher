from Model.DataFormat.PatternMetaData import PatternMetaData


class Pattern:
    def __init__(self, regular_expressions, metadata, del_without_letter, del_without_digit):
        """
        :param regular_expressions: list<str> или str
        :param metadata: PatternMetaData.
        :param del_without_letter: bool.
        :param del_without_digit: bool.
        """
        if isinstance(regular_expressions, str):
            self.__regexes = [regular_expressions]
        else:
            self.__regexes = regular_expressions
        self.__metadata = metadata
        self.__del_without_letter = del_without_letter
        self.__del_without_digit = del_without_digit

    def get_regex(self, i):
        """
        :param i: int. индекс выражения в массиве
        :return: str.
        """
        return self.__regexes[i]

    def get_metadata(self):
        """
        :return: PatternMetaData.
        """
        return self.__metadata

    def is_del_without_letter(self):
        """
        :return: bool
        """
        return self.__del_without_letter

    def is_del_without_digit(self):
        """
        :return: bool
        """
        return self.__del_without_digit

    @classmethod
    def from_dict(cls, dict_data):
        """
        Создание объекта класса по сериализованному словарю
        :param dict_data: dict{regular_expressions: .., metadata: .., del_without_letter: .., del_without_digit: ..}
        :return: Pattern
        """
        try:
            return cls(
                regular_expressions=dict_data["regular_expressions"],
                metadata=PatternMetaData.from_dict(dict_data["metadata"]),
                del_without_letter=dict_data["del_without_letter"],
                del_without_digit=dict_data["del_without_digit"]
            )
        except Exception as ex:
            raise ex

    def to_dict(self):
        """
        Получение сериализованного словаря по объекту
        :return: dict{regular_expressions: .., metadata: .., del_without_letter: .., del_without_digit: ..}
        """
        try:
            return {
                "regular_expressions": self.__regexes,
                "metadata": self.__metadata.to_dict(),
                "del_without_letter": self.__del_without_letter,
                "del_without_digit": self.__del_without_digit
            }
        except Exception as ex:
            raise ex
