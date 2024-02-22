"""Implementation of the Parsers class"""

from datetime import datetime

from json import loads as parser_json_types


class Parsers:
    """Set of Parsers"""

    def __init__(self) -> None:
        self.parsers = {
            'str': (self._convert_to_str, 1),
            'int': (self._convert_to_int, 1),
            'float': (self._convert_to_float, 1),
            'bool': (self._convert_to_bool, 1),
            'none': (self._convert_to_none, 0),
            'dict': (self._convert_to_dict, 1),
            'list': (self._convert_to_list, 1),
            'datetime': (self._convert_to_datetime, 2),
        }

    def get_parser(self, key: str):
        """Returns parser.

        Args:
            key (str): Data type.

        Raises:
            TypeError: If data type does not exist.

        Returns:
            tuple: Returns converter and number of arguments as (function, int).
        """

        try:
            return self.parsers[key]
        except KeyError as exc:
            raise TypeError(f"The data type '{key}' is not defined") from exc

    def set_parser(self, key: str, parser: tuple):
        """Set a new parser.

        Args:
            key (str): Data type.
            parser (tuple): A tuple containing the parser as (converter, number of arguments).
        """

        if not isinstance(key, str):
            raise KeyError("The key must be a string")
        if not len(parser) == 2 or not callable(parser[0]) or \
                not isinstance(parser[1], int) or parser[1] >= 0:
            raise ValueError("The parser must be a tuple containing a "
                             "function and an integer")
        self.parsers.update({key: parser})

    def _convert_to_str(self, value: str):
        return self._convert_to_json_types(value=value, data_type=str)

    def _convert_to_int(self, value: str):
        return self._convert_to_json_types(value=value, data_type=int)

    def _convert_to_float(self, value: str):
        return self._convert_to_json_types(value=value, data_type=float)

    def _convert_to_bool(self, value: str):
        return self._convert_to_json_types(value=value, data_type=bool)

    def _convert_to_none(self):
        return

    def _convert_to_dict(self, value: str):
        return self._convert_to_json_types(value=value, data_type=dict)

    def _convert_to_list(self, value: str):
        return self._convert_to_json_types(value=value, data_type=list)

    def _convert_to_json_types(self, value: str, data_type):
        value_parsed = parser_json_types(value)

        if isinstance(value_parsed, data_type):
            return value_parsed

        raise ValueError(f"The value '{value_parsed}' is not of the "
                         "specified data type")

    def _convert_to_datetime(self, value: str, _format):
        value = self._convert_to_str(value)
        return datetime.strptime(value, _format)
