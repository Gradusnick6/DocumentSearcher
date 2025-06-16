import os

from Model.DirectoryWork.HandlerByOS import handler_by_os
import ViewModel


class SystemDirectoryHandler:
    @staticmethod
    def get_files(directory, file_formats):
        """
        :param directory: str. директория, из которой производится поиск файлов
        :param file_formats: str. формат файла, например, "json"
        :return: list<str>. Относительных путей к файлу, не включая directory
        """
        try:
            files = SystemDirectoryHandler.__get_file_list_recursive(directory)
            file_list = []
            for full_file_name in files:
                split_list = full_file_name.split(".")
                if split_list[-1] in file_formats:
                    path_from_dir = SystemDirectoryHandler.__get_unique_suffix(directory, full_file_name)
                    file_list.append(handler_by_os.get_file_path(path_from_dir))
            return file_list
        except Exception as ex:
            raise ex

    @staticmethod
    def __get_file_list_recursive(directory):
        """
        :param directory: str. директория, из которой производится поиск файлов
        :return: list<str>. Абсолютных путей к файлу, не включая directory
        """
        try:
            file_list = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_name = os.path.join(root, file)
                    if '~$' in file_name:  # пропускать временные-зависшие файлы
                        continue
                    file_list.append(file_name)
            return file_list
        except Exception as ex:
            raise ex

    @staticmethod
    def __get_unique_suffix(str1, str2):
        """
        :return: str. уникальную часть str2 (если начало str2 полностью повторяет str1, иначе возвращает str2
        """
        try:
            if str2.startswith(str1):
                return str2[len(str1) + 1:]  # +1 удаляет слэш
            else:
                return str2
        except Exception as ex:
            raise ex

    @staticmethod
    def get_unique_name_for_exist_file(file_path):
        """
        :param file_path: str. Полное имя файла
        :return: str. Возвращает уникальное полное имя файла
        """
        try:
            directory, file_name = os.path.split(file_path)
            name, ext = os.path.splitext(file_name)

            if not os.path.exists(file_path):
                return file_path

            counter = 1
            new_file_path = os.path.join(directory, f"{name} ({counter}){ext}")
            while os.path.exists(new_file_path):
                counter += 1
                new_file_path = os.path.join(directory, f"{name} ({counter}){ext}")

            ViewModel.message_list.add_info_message(
                f"Файл {file_path} существует. Данные будут записаны в новый файл {new_file_path}")
            return new_file_path
        except Exception as ex:
            raise ex
