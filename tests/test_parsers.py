import unittest
import json
import datetime

from grigode_env import Parsers


class TestParsers(unittest.TestCase):

    def test_str(self):
        """Test convert to str"""

        parser = Parsers().get_parser('str')[0]

        self.assertEqual(parser('"foo"'), 'foo')
        self.assertEqual(parser('"hello world"'), 'hello world')
        self.assertEqual(parser('"125.5"'), '125.5')

    def test_int(self):
        """Test convert to int"""

        parser = Parsers().get_parser('int')[0]

        self.assertEqual(parser('25'), 25)
        self.assertEqual(parser('-25'), -25)

        with self.assertRaises(ValueError):
            self.assertEqual(parser('125.89'), 125)

        with self.assertRaises(json.decoder.JSONDecodeError):
            self.assertEqual(parser('foo'), -1)

    def test_float(self):
        """Test convert to int"""

        parser = Parsers().get_parser('float')[0]

        self.assertEqual(parser('25.5'), 25.5)
        self.assertEqual(parser('-25.5'), -25.5)

        with self.assertRaises(json.decoder.JSONDecodeError):
            self.assertEqual(parser('foo'), -1)

    def test_bool(self):
        """Test convert to int"""

        parser = Parsers().get_parser('bool')[0]

        self.assertTrue(parser('true'))
        self.assertFalse(parser('false'))

    def test_none(self):
        """Test convert to None"""

        parser = Parsers().get_parser('none')[0]

        self.assertIsNone(parser())
        self.assertIsNone(parser())

    def test_dict(self):
        """Test convert to dict"""

        parser = Parsers().get_parser('dict')[0]

        self.assertEqual(parser('{"key": "value"}'), {"key": "value"})

    def test_list(self):
        """Test convert to list"""

        parser = Parsers().get_parser('list')[0]

        self.assertEqual(parser('["foo", 15, 30.5]'), ["foo", 15, 30.5])

    def test_datetime(self):
        """Test convert to datetime"""

        parser = Parsers().get_parser('datetime')[0]

        time, _format = '09/19/22 13:55:26', '%m/%d/%y %H:%M:%S'

        self.assertEqual(parser(f'"{time}"', _format),
                         datetime.datetime.strptime(time, _format))
