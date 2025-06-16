from Model.SaveResult.WriterType import WriterType
from Model.SaveResult.DataForWriteHandler import DataForWriteHandler
from Model.SaveResult.ExcelWriter import ExcelWriter
from Model.SaveResult.StatisticsCalculator import StatisticsCalculator
import ViewModel

import ViewModel


class ResultWriter:
    def __init__(self, writer_type, config_container, loger):
        """
        Исключения: TypeError()
        :param writer_type: WriterType
        :param config_container: ConfigContainer
        :param loger: MessageSaver
        :return: None
        """
        if isinstance(writer_type, WriterType):
            self.__writer_type = writer_type
            self.__config_container = config_container
            self.__logger = loger
        else:
            raise TypeError()

    def write(self, file_path, data):
        """
        :param file_path: str
        :param data: PatternStringDict<string, PatternStringList<...>>
        :return: None
        """
        try:
            statistic_dict = self.__get_info_data(data)
            handled_data = DataForWriteHandler.handle_data(data, self.__writer_type)
            handled_data = dict(sorted(handled_data.items()))

            handled_statistic = DataForWriteHandler.handle_static_data(statistic_dict)
            handled_metainfo = {"Статистика": self.__get_metainfo_data() + handled_statistic["Статистика"]}
            data_for_write = handled_metainfo | handled_data

            #  количество листов + форматирование
            ViewModel.multi_progress_bar.start_next_process(len(data_for_write.keys()) + 1)

            writer = ExcelWriter()
            writer.write(file_path, data_for_write)
        except Exception as ex:
            raise ex

    def __get_info_data(self, data):
        """
        :return: data<string, dict<string, ...>>
        """
        try:
            ViewModel.message_list.add_info_message(f"Вычисляю статистические данные")
            calculator = StatisticsCalculator(data, self.__config_container)
            info_dict = {
                "Найдено тэгов по листам этого документа": calculator.get_count_str_by_sheet(),
                "Найдено уникальных тэгов по листам этого документа": calculator.get_count_unique_str_by_sheet(),
                "Найдено уникальных тэгов в документе по именам паттерна": calculator.get_count_unique_str_by_pattern_name(),
                "Найдено уникальных тэгов в документе по типу паттерна": calculator.get_count_unique_str_by_type()
            }
            return info_dict
        except Exception as ex:
            raise ex

    def __get_metainfo_data(self):
        metainfo_list = [
            ["Входные данные для поиска", "Первый regex просматривал", self.__config_container.source_file]
        ]
        if self.__config_container.is_search:
            metainfo_list.append(["", "Поиск выгруженных строк производился в"] + self.__config_container.search_files)
        metainfo_list.append(["", "Логи загружены в файл", self.__logger.get_file_path()])
        metainfo_list.append([""])
        metainfo_list.append(
            ["",
             "Паттерны",
             "Имя паттерна",
             "Тип",
             "Regex №1",
             "Regex №2",
             "Удаляем строки без букв",
             "Удаляем строки без цифр"]
        )

        counter = 1
        for pattern in self.__config_container.pattern_list:
            metainfo_list.append(["",
                                  str(counter),
                                  pattern.get_metadata().get_name(),
                                  pattern.get_metadata().get_type().name,
                                  pattern.get_regex(0),
                                  pattern.get_regex(1) if self.__config_container.is_search else "Не используется",
                                  str(pattern.is_del_without_letter()),
                                  str(pattern.is_del_without_digit())
                                  ])
            counter += 1

        metainfo_list.append([""])
        return metainfo_list
