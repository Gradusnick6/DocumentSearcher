from Model.SaveResult import ResultWriter, WriterType
from Model.TagGeneration import PatternSearcherFacade
from Model.Search import PatternStringSearcher
from Model.DataFormat import UpgradeArgumentBox, PatternStringForSearch, SortType
from Model.Message import MessageSaver

import ViewModel

import traceback


def search_and_save_by_config(config_path):
    """
    Основной сценарий программы
    :param config_path: str
    :return: None
    """
    loger = MessageSaver()
    try:
        config_container = ViewModel.init_input(config_path)
        ViewModel.message_list.add_info_message("Данные из конфиг файла успешно считаны")
        source_file = config_container.source_file
        pattern_list = config_container.pattern_list
        result_file = config_container.result_file
        is_search = config_container.is_search

        ViewModel.message_list.add_info_message(f"Читаю тэги из файла {source_file}")
        psdict_for_search = regex_search(source_file, pattern_list)
        ViewModel.message_list.add_info_message(f"Список тэгов из файла {source_file} успешно считан")
        if is_search:
            search_files = config_container.search_files
            ViewModel.message_list.add_info_message(f"Начинаю искать строки в других файлах. "
                                                    f"Всего файлов {len(search_files)} шт.")
            data_for_write = pattern_string_search(search_files, psdict_for_search, pattern_list)
            writer_type = WriterType.WRITE_SEARCH_RESULT
            ViewModel.message_list.add_info_message("Закончил искать строки в других файлах")
        else:
            data_for_write = psdict_for_search
            writer_type = WriterType.WRITE_PATTERN_STRINGS

        ViewModel.message_list.add_info_message(f"Начинаю записывать результаты в файл {result_file}")
        excel_writer(result_file, data_for_write, writer_type, config_container, loger)
        ViewModel.message_list.add_info_message(f"Данные успешно записаны")
    except Exception as ex:
        if len(ex.args) == 1:
            add_error_msg(ex)
    finally:
        log_filename = loger.save_to_file(ViewModel.message_list)
        ViewModel.message_list.set_zero_lvl()
        ViewModel.message_list.add_info_message(f"Логи успешно записаны в {log_filename}")
        if ViewModel.manager_multi_process is not None:
            ViewModel.manager_multi_process.shutdown()


def regex_search(source_file, pattern_list):
    """
    Считывание тэгов из source_file
    :param source_file: str
    :param pattern_list: PatternList
    :return: PatternStringDict<string, PatternStringList<PatternStringForSearch>>
    """
    try:
        ViewModel.message_list.increment_lvl()
        pstrings = PatternSearcherFacade.get_pattern_string_from_file(source_file, pattern_list)
        ViewModel.message_list.decrement_lvl()
        return pstrings
    except Exception as ex:
        raise ex


def pattern_string_search(search_files, psdict, pattern_list):
    """
    Поиск строк по search_files
    :param search_files: list<str>
    :param psdict: PatternStringDict<string, PatternStringList<PatternString>>
    :param pattern_list: PatternList
    :return: PatternStringDict<string, PatternStringList<PatternStringSearchResult>>
    """
    try:
        ViewModel.message_list.increment_lvl()
        args_dict = {}
        for pattern in pattern_list:
            metadata = pattern.get_metadata()
            args_dict[metadata.get_name()] = pattern.get_regex(1)
        upgrade_box = UpgradeArgumentBox(PatternStringForSearch, args_dict)
        psdict.upgrade_item_type(upgrade_box)
        ps_searcher = PatternStringSearcher(search_files, psdict)
        searched_data = ps_searcher.search()
        ViewModel.message_list.decrement_lvl()
        return searched_data
    except Exception as ex:
        raise ex


def excel_writer(result_file, data, writer_type, config_container, loger):
    """
    Запись результатов работы программы в result_file
    :param result_file: str
    :param data: PatternStringDict. Результаты работы программы
    :param writer_type: WriterType. Тип записи в файл
    :param config_container: ConfigContainer
    :param loger: MessageSaver
    :return: None
    """
    try:
        ViewModel.message_list.increment_lvl()
        data.sort(SortType.BY_STRING)
        data.sort(SortType.BY_PATTERN_TYPE)
        writer = ResultWriter(writer_type, config_container, loger)
        writer.write(result_file, data)
        ViewModel.message_list.decrement_lvl()
    except Exception as ex:
        raise ex


def add_error_msg(ex):
    """
    Выводит сообщение об ошибке, мешающей работе программы
    :param ex: Exception
    :return: None
    """
    # Извлекаем информацию о стеке вызова
    tb = ex.__traceback__
    stack_summary = traceback.extract_tb(tb)
    # Формируем строку в нужном формате
    offset_str = "\n ->              "
    stack_trace_str = offset_str.join(
        f"File {frame.filename}, Line {frame.lineno}" for frame in stack_summary
    )

    msg_text = ex.args[0] + offset_str + stack_trace_str  # ex.args - tuple
    ViewModel.message_list.add_crit_error_message(msg_text)
