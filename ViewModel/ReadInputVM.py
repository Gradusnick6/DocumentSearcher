import ViewModel
from Ui.ConfigFile.ConsoleLogs import ConsoleLogs
from Ui.ConfigFile.ConsoleProgressBar import ConsoleProgressBar
from Ui.ConfigFile.ConfigContainer import ConfigContainer

from Model.Service import MultiProcessManager
from Model.Service.ProgressBar import MultiProcessProgressBar
from Model.DataFormat import PatternType, PatternMetaData, PatternList, Pattern
from Model.Message import MessageList
from Model.DirectoryWork import SupportedFileExtension

import os
import json


def init_input(config_path):
    """
    Инициализирует переменные глобального контекста "GlobalContext.py"
    Считывает данные из config-файла и возвращает в виде объекта ConfigContainer
    :param config_path: str. Путь к конфиг файлу
    """
    try:
        init_manager_and_logs()
        config_container = read_or_create_config(config_path)
        check_files_exist(config_container)
        set_multi_progress_bar(config_container)
        return config_container
    except Exception as ex:
        raise ex


def init_manager_and_logs():
    """
    Инициализирует переменные глобального контекста "GlobalContext.py"
    :return: None
    """
    try:
        MultiProcessManager.register('MessageList', MessageList)
        MultiProcessManager.register('ConsoleLogs', ConsoleLogs)
        MultiProcessManager.register('MultiProcessProgressBar', MultiProcessProgressBar)

        manager = MultiProcessManager()
        manager.start()

        ViewModel.manager_multi_process = manager
        ViewModel.operating_log = manager.ConsoleLogs()  # инициализируем глобальный принтер логов
        ViewModel.message_list = manager.MessageList(ViewModel.operating_log)
        ViewModel.operating_log.print_header(ViewModel.message_list.get_header())
    except Exception as ex:
        raise ex


def read_or_create_config(config_path):
    """
    :param config_path: str
    :return: ConfigContainer
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                obj_dict = json.load(f)
            config_container = ConfigContainer.from_dict(obj_dict)
            config_container.search_files = list(set(config_container.search_files))
            return config_container
        else:
            template_dict = get_template_dict()
            with open(config_path, 'w') as f:
                json.dump(template_dict, f, indent=4)
            raise FileNotFoundError("Файл конфигурации не найден. Исследование не произведено, "
                                    "но файл пересоздан :3\n Заполни, пж, файл config_ds_v2.json")
    except Exception as ex:
        raise ex


def get_template_dict():
    """
    Возвращает стандартные значения для нового конфиг файла
    :return: dict
    """
    try:
        source_file = "input\\__.pdf"
        str_1 = r"[a-zA-Z0-9]{1,}_[a-zA-Z0-9]{2,}\.?[\d]?(?:/\d{4}+[A-Z]*)*"
        str_2 = r"0[\d]{2}_[a-zA-Z0-9]+_[\d]{3,4}\.?[\d]?[A-Z]?(?:/\d{4}+[A-Z]*)*"
        str_1_1 = r"[a-zA-Z0-9]{1,}_[a-zA-Z0-9]{2,}\.?[\d]?(?:/\d{4}+[A-Z]*)*"
        str_2_1 = r"0[\d]{2}_<sP>[a-zA-Z0-9]+_<eP>[\d]{3,4}\.?[\d]?[A-Z]?(?:/\d{4}+[A-Z]*)*"
        patterns = PatternList(
            [Pattern([str_2, str_2_1], PatternMetaData("pattern 1", PatternType.GOOD), True, False),
             Pattern([str_1, str_1_1], PatternMetaData("pattern 2", PatternType.WARNING), True, False)])
        search_files = ["input\\_1.xlsm", "input\\_2.xlsm"]
        result_file = "output\\__.xlsx"
        is_search = True
        config = ConfigContainer(source_file, patterns, search_files, result_file, is_search)
        return config.to_dict()
    except Exception as ex:
        raise ex


def check_files_exist(config_container):
    """
    Проверка наличия и формата входных файлов
    :param config_container: ConfigContainer
    :return: None
    """
    error_msg_list = []
    try:
        error_msg_list.append(get_error_msg_by_check_file_exist(config_container.source_file,
                                                                "source_file",
                                                                SupportedFileExtension.get_source_extensions()))
        if config_container.is_search:
            for file_path in config_container.search_files:
                error_msg_list.append(get_error_msg_by_check_file_exist(file_path,
                                                                        "search_files",
                                                                        SupportedFileExtension.get_for_search_extensions()))
        error_msg_list = [x for x in error_msg_list if x != ""]
        if len(error_msg_list) > 0:
            raise FileExistsError()
    except FileExistsError:
        for msg_str in error_msg_list:
            ViewModel.message_list.add_error_message(msg_str)
        raise Exception("", "")
    except Exception as ex:
        raise ex


def get_error_msg_by_check_file_exist(file_path, file_role, extension_list):
    """
    Возвращает строку-ошибку. Если возвращает пустую строку, файл указан корректно
    :param file_path: str. Путь к файлу
    :param file_role: str. Используется для описание роли файла, если возникнет ошибка
    :param extension_list: list<str>. Список разрешенных расширений файла
    :return: str
    """
    try:
        if not os.path.exists(file_path):
            return f"{file_role}. {file_path} отсутсвует"
        file_extension = file_path.split('.')[-1]
        if file_extension not in extension_list:
            extension_str = ", ".join(extension_list)
            return f"{file_role}. {file_path} не соответствует требуемым типам файла: {extension_str}"
        return ""
    except Exception as ex:
        raise ex


def set_multi_progress_bar(config_container):
    """
    Инициализирует прогресс бары процессами из config-файла
    :param config_container: ConfigContainer
    :return: None
    """
    try:
        count_search_files = len(config_container.search_files)
        progress_bar_list = [ConsoleProgressBar(ViewModel.message_list),
                             # поиск тэгов с использованием regex по source_file
                             ConsoleProgressBar(ViewModel.message_list)]  # запись результата в result_file

        if config_container.is_search:
            # поиск тэгов в уникальных search_files
            progress_bar_list += [ConsoleProgressBar(ViewModel.message_list) for i in range(count_search_files)]

        process_names = [f"чтение тэгов по регулярным выражениям из файла {config_container.source_file}"]
        if config_container.is_search:
            process_names += [f"поиск строк в {path}" for path in config_container.search_files]
        process_names += [f"запись результатов в файл"]

        manager = ViewModel.manager_multi_process
        ViewModel.multi_progress_bar = manager.MultiProcessProgressBar(progress_bar_list,
                                                                       process_names,
                                                                       ViewModel.message_list)
    except Exception as ex:
        raise ex
