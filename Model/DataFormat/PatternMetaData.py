from Model.DataFormat.PatternType import PatternType


class PatternMetaData:
    def __init__(self, name, pattern_type):
        """
        :param name: str
        :param pattern_type: PatternType
        """
        self.__name = name
        self.__type = pattern_type

    def __eq__(self, other):
        if isinstance(other, PatternMetaData):
            return self.__name == other.__name and self.__type == other.__type
        return False

    def __hash__(self):
        return hash(self.__name) + hash(self.__type)

    def get_metainfo_list(self):
        """
        :return: list<str>
        """
        return [self.__name, self.__type.name]

    def get_name(self):
        """
        :return: str
        """
        return self.__name

    def get_type(self):
        """
        :return: PatternType
        """
        return self.__type

    @classmethod
    def from_dict(cls, dict_data):
        """
        Создание объекта класса по сериализованному словарю
        :param dict_data: dict{name: .., type: ..}
        :return: PatternMetaData
        """
        try:
            pt = PatternType[dict_data["type"]]  # Десериализация enum
            return cls(
                name=dict_data["name"],
                pattern_type=pt
            )
        except Exception as ex:
            raise ex

    def to_dict(self):
        """
        Получение сериализованного словаря по объекту
        :return: dict{name: .., type: ..}
        """
        return {
            "name": self.__name,
            "type": self.__type.name
        }
