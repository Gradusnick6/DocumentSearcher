from Model.DataFormat.PatternString import PatternString
from Model.DataFormat.Pattern import Pattern
from Model.DataFormat.RegexGenerator import RegexGenerator


class PatternStringForSearch(PatternString):
    def __init__(self, string=None, metadata=None, regex=None, arg_box=None):
        """
        Заполнять либо только string, metadata и pattern_str либо только arg_box
        Исключения: TypeError, ValueError
        :param string: str
        :param metadata: PatternMetaData
        :param regex: str
        :param arg_box: obj - PatternString  args - dict[]. key: str   - pattern name
                                                            value: str - regex
        """
        try:
            if not (string is None) and not (metadata is None) and not (regex is None):
                self.__default_init(string, metadata, regex)
            elif not (arg_box is None):
                self.__copy_init(arg_box)
            else:
                raise ValueError()
        except Exception as ex:
            raise ex

    def __default_init(self, string, metadata, regex):
        if isinstance(string, str):
            self.__pattern = self.__create_pattern(regex)
            self._default_init(string, metadata)
        else:
            raise TypeError()

    def __copy_init(self, arg_box):
        try:
            base_obj = arg_box.obj
            self._copy_init(arg_box)
            regex_dict = arg_box.args
            if not isinstance(regex_dict, dict):
                raise TypeError()
            this_name = base_obj.get_metadata().get_name()
            if this_name in regex_dict:
                self.__pattern = self.__create_pattern(regex_dict[this_name])
            else:
                raise ValueError()
        except Exception as ex:
            raise ex

    def __create_pattern(self, regex):
        """
        :param regex: str
        :return: Pattern
        """
        try:
            regex_generator = RegexGenerator()
            regex_for_pattern = regex_generator.create_regex(self.get_string(), regex)
            return Pattern(regex_for_pattern, self._metadata, False, False)
        except Exception as ex:
            raise ex

    def get_regex(self):
        """
        :return: str
        """
        try:
            return self.__pattern.get_regex(0)
        except Exception as ex:
            raise ex
