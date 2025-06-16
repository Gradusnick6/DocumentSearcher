from Model.SaveResult.WriterType import WriterType
from Model.DataFormat.PatternStringDict import PatternStringDict
from Model.SaveResult.HeadersForWrite import headers_for_write_dict


class DataForWriteHandler:
    @staticmethod
    def handle_data(pattern_string_dict, writer_type):
        """
        Преобразует данные в удобоваримый для записи в эксель вид
        Исключения: TypeError()
        :param pattern_string_dict: PatternStringDict
        :param writer_type: WriterType
        :return: dict<list<list<str/float/int>>>
        """
        if isinstance(writer_type, WriterType) or isinstance(pattern_string_dict, PatternStringDict):
            if writer_type == WriterType.WRITE_SEARCH_RESULT:
                return DataForWriteHandler.__handle_search_result(pattern_string_dict)
            if writer_type == WriterType.WRITE_PATTERN_STRINGS:
                return DataForWriteHandler.__handle_pattern_string(pattern_string_dict)
        else:
            raise TypeError()

    @staticmethod
    def handle_static_data(statistic_data):
        """
        Преобразует данные о статистике в удобоваримый для записи в эксель вид
        :param statistic_data: dict<string, dict<string, ...>>
        :return: dict<list<list<str>>>
        """
        try:
            matrix_data = DataForWriteHandler.__get_listliststr_by_dict_recursive(statistic_data, 0)
            return {"Статистика": matrix_data}
        except Exception as ex:
            raise ex

    @staticmethod
    def __handle_search_result(pattern_string_dict):
        """
        :param pattern_string_dict: PatternStringDict<PatternStringList<...>>
        :return: dict<list<list<str/float/int>>>
        """
        try:
            result_dict = {}
            sheet_names = DataForWriteHandler.get_sheet_names(pattern_string_dict)
            for sheet_name in sheet_names:
                sheet_matrix = [headers_for_write_dict[WriterType.WRITE_SEARCH_RESULT]]
                for key, pslist in pattern_string_dict.items():
                    sheet_matrix.append(["", "", "", f"__PAGE_{str(key)}__"])
                    for ps in pslist:
                        if sheet_name in ps.get_unique_group_names():
                            sheet_matrix.append(ps.get_param_list(sheet_name))
                    sheet_matrix.append([""])
                result_dict[sheet_name] = sheet_matrix

            not_find_matrix = [headers_for_write_dict[WriterType.NOT_FOUND]]
            for key, pslist in pattern_string_dict.items():
                not_find_matrix.append(["", "", "", f"__PAGE_{str(key)}__"])
                for ps in pslist:
                    param_list = ps.get_param_list()
                    if ps.is_empty_searched_result():
                        not_find_matrix.append(param_list)
                not_find_matrix.append([""])
            result_dict["Не найдено"] = not_find_matrix
            return result_dict
        except Exception as ex:
            raise ex

    @staticmethod
    def __handle_pattern_string(pattern_string_dict):
        """
        :param pattern_string_dict: PatternStringDict<PatternStringList<...>>
        :return: dict<list<list<str/float/int>>>
        """
        try:
            matrix_data = [headers_for_write_dict[WriterType.WRITE_PATTERN_STRINGS]]
            for key, value in pattern_string_dict.items():
                matrix_data.append(["", "", "", f"__PAGE_{str(key)}__"])
                for pattern_string in value:
                    matrix_data.append(pattern_string.get_param_list())
                matrix_data.append([""])
            return {"Тэги": matrix_data}
        except Exception as ex:
            raise ex

    @staticmethod
    def get_sheet_names(pattern_string_dict):
        """
        :param pattern_string_dict: PatternStringDict<PatternStringList<PatternStringSearchResult>>
        :return: list<str>
        """
        try:
            sheet_name_list = []
            for key, pslist in pattern_string_dict:
                for ps in pslist:
                    ps.calculate_unique_group_names()
                    unique_group_names = ps.get_unique_group_names()
                    for group_name in unique_group_names:
                        sheet_name_list.append(group_name)
            sheet_name_set = set(sheet_name_list)
            return list(sheet_name_set)
        except Exception as ex:
            raise ex

    @staticmethod
    def __get_listliststr_by_dict_recursive(data_dict, lvl_input):
        """
        Возвращает матрицу строк по словарю. Рекурсивно, если значение - словарь
        :param data_dict: data<string, dict<string, ...>>
        :param lvl_input: int определяет глубину ухода в рекурсию
        :return: list<list<str>>
        """
        try:
            result = []
            for key, value in data_dict.items():
                if isinstance(value, dict):
                    if len(result) == 0:
                        result = [[str(key)]]
                    else:
                        result.append([""] * lvl_input + [str(key)])
                    child_list = DataForWriteHandler.__get_listliststr_by_dict_recursive(value, lvl_input + 1)

                    if len(child_list) > 0:
                        result[len(result) - 1] += child_list[0]
                    if len(child_list) > 1:
                        result += child_list[1:]

                else:
                    if len(result) == 0:
                        result = [[str(key), str(value)]]
                    else:
                        result.append([""] * lvl_input + [str(key), str(value)])

                if lvl_input == 0:
                    result.append([""])
                    result.append([""])
            return result
        except Exception as ex:
            raise ex
