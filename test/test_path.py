
from unittest import TestCase
from nose_parameterized import parameterized

from piriti.path import Path
from piriti.exceptions import InvalidPath

class TestPath(TestCase):

    @parameterized.expand([
        ('simple', '/node1/node2/node3', ['/', '/node1', '/node1/node2', '/node1/node2/node3']),
        ('root', '/', ['/']),
    ])
    def test_sub_path(self, name, input, expected):
        # Arrange
        path = Path(input)

        # Act
        sub_path = list(path.get_all_sub_path())

        # Assert
        self.assertEqual(sub_path, expected)

    @parameterized.expand([
        ('empty', ''),
        ('None', None),
    ])
    def test_sub_path_error(self, name, input):
        # Arrange & Act & Assert
        with self.assertRaises(InvalidPath):
            Path('')
