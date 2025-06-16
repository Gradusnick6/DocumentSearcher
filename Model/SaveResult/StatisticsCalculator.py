from Model.DataFormat import PatternString, PatternStringSearchResult
from Model.SaveResult.DataForWriteHandler import DataForWriteHandler


class StatisticsCalculator:
    def __init__(self, data, config_container):
        """
        :param data: PatternStringDict
        :param config_container: ConfigContainer
        """
        self.__sheet_name_list,  self.__data_dict = self.__get_listdict_from_dict(data)
        self.__config_container = config_container

    def get_count_str_by_sheet(self):
        """
        Рассчитывает количество pattern_string
        :return: dict<string, int>
        """
        try:
            result = {}
            for idata in range(len(self.__data_dict)):
                sheet_name = self.__sheet_name_list[idata]
                result[sheet_name] = len(self.__data_dict[sheet_name])
            return result
        except Exception as ex:
            raise ex

    def get_count_unique_str_by_sheet(self):
        """
        Рассчитывает количество уникальных pattern_string
        :return: dict<string, int>
        """
        try:
            result = {}
            full_string_list = []
            for idata in range(len(self.__data_dict)):
                sheet_name = self.__sheet_name_list[idata]
                full_string_list += self.__data_dict[sheet_name]
                result[sheet_name] = len(set([ps.get_string() for ps in self.__data_dict[sheet_name]]))
            full_string_set = set([ps.get_string() for ps in full_string_list])
            result["Общее количество"] = len(full_string_set)
            return result
        except Exception as ex:
            raise ex

    def get_count_unique_str_by_pattern_name(self):
        """
        Рассчитывает количество уникальных pattern_string по именам паттерна
        :return: dict<string, dict<string, int>>
        """
        try:
            result = {}
            for sheet_name in self.__sheet_name_list:
                result[sheet_name] = {}
            result["Общее количество"] = {}

            for key in result.keys():
                for pname in self.__config_container.pattern_list.get_unique_name_list():
                    result[key][pname] = 0

            full_string_list = []
            for idata in range(len(self.__data_dict)):
                sheet_name = self.__sheet_name_list[idata]
                full_string_list += self.__data_dict[sheet_name]
                for ps in set(self.__data_dict[sheet_name]):
                    result[sheet_name][ps.get_metadata().get_name()] += 1

            for ps in set(full_string_list):
                result["Общее количество"][ps.get_metadata().get_name()] += 1
            return result
        except Exception as ex:
            raise ex

    def get_count_unique_str_by_type(self):
        """
        Рассчитывает количество уникальных pattern_string по качеству паттерна
        :return: dict<string, dict<string, int>>
        """
        try:
            result = {}
            for sheet_name in self.__sheet_name_list:
                result[sheet_name] = {}
            result["Общее количество"] = {}

            for key in result.keys():
                for ptype in self.__config_container.pattern_list.get_unique_type_list():
                    result[key][ptype.name] = 0

            full_string_list = []
            for idata in range(len(self.__data_dict)):
                sheet_name = self.__sheet_name_list[idata]
                full_string_list += self.__data_dict[sheet_name]
                for ps in set(self.__data_dict[sheet_name]):
                    result[sheet_name][ps.get_metadata().get_type().name] += 1

            for ps in set(full_string_list):
                result["Общее количество"][ps.get_metadata().get_type().name] += 1
            return result
        except Exception as ex:
            raise ex

    def __get_listdict_from_dict(self, data):
        """
        Возвращает список словарей паттерновых строк относительно хранимой структуры data
        :return: (list<str>, dict<string, list<PatternString>>)
        """
        result_values = {}
        result_keys = []
        any_value = None

        try:
            for key, pslist in data:
                if len(pslist) > 0:
                    any_value = pslist[0]
                    break
            if any_value is None:
                raise Exception("Не найдено тэгов в искомой PDF, невозможно подсчитать статистику. Файл не создам")

            elif isinstance(any_value, PatternStringSearchResult):  # Если искали тэги по другим файлам
                result_keys = DataForWriteHandler.get_sheet_names(data)
                result_keys.append("Не найдено")

                for key in result_keys:
                    result_values[key] = []

                for key, pslist in data:
                    for ps in pslist:
                        sheet_names = ps.get_unique_group_names()  # места, где был найден тэг
                        if len(sheet_names) > 0:
                            for name in sheet_names:  # добавляем в тэг во все списки, где он был найден
                                result_values[name].append(ps)
                        else:  # если мест нет, он не найден
                            result_values["Не найдено"].append(ps)

            if isinstance(any_value, PatternString):  # Если не искали тэги по другим файлам
                result_values["Тэги"] = []
                for key, pslist in data:
                    for ps in pslist:
                        result_values["Тэги"].append(ps)
                result_keys.append("Тэги")

            return result_keys, result_values
        except Exception as ex:
            raise ex
