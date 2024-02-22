"""Implementation of the Environ class"""

import os
import json

from grigode_env import errors, types
from grigode_env.parsers import Parsers

EnvironPath = str | types.IterableStr


class Environ:
    """Class for handling environment variables"""

    EQUAL = '='
    COMMENT = '#'
    KEY_SEPARATOR = ':'

    def __init__(
        self,
        path: EnvironPath,
        parsers: Parsers = Parsers(),
        merge_files: bool = True,
        **kwars
    ) -> None:
        self._parsers = parsers
        self.environ = {}
        self.environ.update(os.environ.copy())
        self.environ.update(kwars)
        self.environ.update(self.load_environ(path, merge_files))

    def load_environ(self, path: EnvironPath, merge_files: bool) -> types.DictStrAny:
        """Loading environment variables

        Args:
            path (EnvironPath): Paths of the .env files

        Returns:
            dict: Environment variables from the specified files
        """
        environs: types.DictStrAny = {}
        paths = self._format_paths(path=path)

        for path_formated in paths:
            file_parsed = self._parse_file_content(
                file_content=self._read_env_file(path=path_formated),
                path=path_formated)

            if merge_files:
                environs.update(file_parsed)
            else:
                environs[path_formated] = file_parsed

        return environs

    def get(self, key: str) -> types.Any:
        """Gets the value of an environment variable.

        Args:
            key (str): The key of the environment variable to retrieve.

        Returns:
            Any: The value of the environment variable if it exists, None if not found.
        """
        return self.environ.get(key, None)

    def set_variables(self, variables: dict) -> None:
        """Sets multiple environment variables at once.

        Args:
            variables (dict): A dictionary where the keys are the names of the environment variables
                            and the values are the respective values.
        """
        self.environ.update(variables)

    def _parse_file_content(self, file_content: types.ListStr, path: str):
        variables = {}

        for index, line in enumerate(file_content):
            line = line.strip()

            if line.startswith(self.COMMENT) or not line:
                continue

            if line.count(self.EQUAL) < 0:
                raise SyntaxError(f"Error: Line {index + 1}, file '{path}'. "
                                  "The assignment symbol '=' is required")

            full_key, full_value = line.split(self.EQUAL, 1)

            key_parsed = self._parse_full_key(full_key, index, path)

            key = key_parsed.identifier
            value = self._parse_value(key_parsed, full_value)

            variables[key] = value

        return variables

    def _parse_full_key(self, full_key: str, index: int, path: str) -> types.KeyParsed:
        key_subs = [sub.strip()
                    for sub in full_key.split(self.KEY_SEPARATOR, 2)]

        if not key_subs[0]:
            raise SyntaxError(f"Error: Line {index + 1}, file '{path}'. "
                              "The identifier must be declared")

        identifier = key_subs[0]
        parser = key_subs[1] if len(key_subs) >= 2 else 'none'
        args = json.loads(key_subs[2]) if len(key_subs) == 3 else []

        if not isinstance(args, list):
            raise SyntaxError(f"Error: Line {index + 1}, file '{path}'. "
                              "The arguments must be declared as a list.")

        return types.KeyParsed(identifier, parser, args)

    def _parse_value(self, key_parsed: types.KeyParsed, full_value: str):
        parser, n_args = self._parsers.get_parser(key=key_parsed.parser)

        if n_args == 0:
            return parser()

        return parser(full_value, *key_parsed.args[:n_args-1])

    def _read_env_file(self, path: str) -> types.ListStr:
        with open(path, mode='r', encoding='utf-8') as file:
            return file.read().splitlines()

    def _format_paths(self, path: EnvironPath) -> types.ListStr:
        def validate_path(path: str):
            if path.endswith('.env'):
                return True
            raise errors.InvalidExtensionFile()

        if isinstance(path, str) and validate_path(path):
            return [path]
        if isinstance(path, types.Iterable):
            return [p for p in path if validate_path(p)]

        raise TypeError("The data type of the path parameter must be str or "
                        "Iterable[str]")
