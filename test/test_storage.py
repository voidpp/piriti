
from unittest import TestCase
from nose_parameterized import parameterized

from piriti.path import Path
from piriti.data_pack import DataPack
from piriti.storage import MessageStorageMemory

class TestStorage(TestCase):

    def test_store_memory(self):
        # Arrange
        storage = MessageStorageMemory()
        data = DataPack(Path(), {"value": 42})

        # Act
        res = storage.store(data)

        # Assert
        self.assertTrue(res)
        self.assertEqual(storage._data, {"/": [data]})

    @parameterized.expand([
        # name                 path      data_list, expeced_data_pack_index_list
        ('root',               '/',      [DataPack(Path('/'), 42)], [0]),
        ('tree_match',         '/',      [DataPack(Path('/apple'), 42)], [0]),
        ('simple_match',       '/apple', [DataPack(Path('/apple'), 42), DataPack(Path('/pear'), 42)], [0]),
        ('simple_not_match',   '/apple', [DataPack(Path('/'), 42)], []),
        ('root_tree_multiple', '/',      [DataPack(Path('/'), 42), DataPack(Path('/apple'), 42)], [0, 1]),
    ])
    def test_fetch_memory(self, name, path, data_list, expeced_data_pack_index_list):
        # Arrange
        storage = MessageStorageMemory()
        for data in data_list:
            storage.store(data)

        # Act
        res = storage.fetch(Path(path))

        # Assert
        self.assertEqual(len(res), len(expeced_data_pack_index_list))
        for idx in expeced_data_pack_index_list:
            self.assertEqual(res[idx], data_list[idx])

