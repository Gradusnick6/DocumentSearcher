from Model.DataFormat.PatternMetaData import PatternMetaData
from Model.DataFormat.UpgradeArgumentBox import UpgradeArgumentBox


class PatternString:
    def __init__(self, string=None, metadata=None, arg_box=None):
        """
        Заполнять либо только string и metadata либо только arg_box
        Исключения: TypeError() ValueError()
        :param arg_box: obj - PatternString         args - не используется
        :param string: str
        :param metadata: PatternMetaData
        """
        try:
            if not (string is None) and not (metadata is None):
                self._default_init(string, metadata)
            elif not (arg_box is None):
                self._copy_init(arg_box)
            else:
                raise ValueError()
        except Exception as ex:
            raise ex

    def __eq__(self, other):
        if isinstance(other, PatternString):
            return self._string == other._string and self._metadata == other._metadata
        return False

    def __hash__(self):
        return hash(self._string) + hash(self._metadata)

    def _default_init(self, string, metadata):
        if isinstance(string, str):
            self._string = string
        else:
            raise TypeError()
        if isinstance(metadata, PatternMetaData):
            self._metadata = metadata
        else:
            raise TypeError()

    def _copy_init(self, arg_box):
        if isinstance(arg_box, UpgradeArgumentBox):
            if isinstance(arg_box.obj, PatternString):
                self._default_init(arg_box.obj.get_string(), arg_box.obj.get_metadata())
            else:
                raise TypeError()
        else:
            raise TypeError()

    def get_metadata_list(self):
        """
        :return: list<str>
        """
        return self._metadata.get_metainfo_list()

    def get_metadata(self):
        """
        :return: PatternMetaData
        """
        return self._metadata

    def get_param_list(self):
        """
        :return: list<str>
        """
        try:
            return self._metadata.get_metainfo_list() + [self._string]
        except Exception as ex:
            raise ex

    def get_string(self):
        """
        :return: str
        """
        return self._string
