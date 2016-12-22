
from unittest import TestCase

from piriti.message_distributor import MessageDistributor
from piriti.listener import Listener
from piriti.path import Path
from piriti.data_pack import DataPack

class FakeListener(Listener):

    def __init__(self):
        super(FakeListener, self).__init__(None, lambda x: x)
        self.messages = []

    def send(self, data):
        self.messages.append(data)


class TestDistributor(TestCase):

    def test_dispatch_single_match(self):
        # Arrange
        distrib = MessageDistributor()
        listener = FakeListener()
        distrib.register(Path('/apple'), listener)
        data = {"the_answer": 42}

        # Act
        distrib.dispatch(DataPack(Path('/apple'), data))

        # Assert
        self.assertEqual(len(listener.messages), 1)
        self.assertDictEqual(listener.messages[0]['data'], data)

    def test_dispatch_single_not_match(self):
        # Arrange
        distrib = MessageDistributor()
        listener = FakeListener()
        distrib.register(Path('/apple'), listener)
        data = {"the_answer": 42}

        # Act
        distrib.dispatch(DataPack(Path('/pear'), data))

        # Assert
        self.assertEqual(len(listener.messages), 0)

    def test_dispatch_sub_tree_match(self):
        # Arrange
        distrib = MessageDistributor()
        listener = FakeListener()
        distrib.register(Path('/apple'), listener)
        data = {"the_answer": 42}

        # Act
        distrib.dispatch(DataPack(Path('/apple/core'), data))

        # Assert
        self.assertEqual(len(listener.messages), 1)
        self.assertDictEqual(listener.messages[0]['data'], data)

    def test_dispatch_sub_tree_not_match(self):
        # Arrange
        distrib = MessageDistributor()
        listener = FakeListener()
        distrib.register(Path('/apple/core'), listener)
        data = {"the_answer": 42}

        # Act
        distrib.dispatch(DataPack(Path('/apple'), data))

        # Assert
        self.assertEqual(len(listener.messages), 0)

    def test_register(self):
        # Arrange
        distrib = MessageDistributor()
        listener = FakeListener()
        path = Path('/apple/core')

        # Act
        distrib.register(path, listener)

        # Assert
        self.assertEqual(len(distrib._listeners), 1)
        self.assertEqual(distrib._listeners['/apple/core'], [listener])


    def test_unregister(self):
        # Arrange
        distrib = MessageDistributor()
        listener = FakeListener()
        path = Path('/apple/core')
        distrib.register(path, listener)
        self.assertEqual(len(distrib._listeners), 1)

        # Act
        res = distrib.unregister(listener)

        # Assert
        self.assertTrue(res)
        self.assertEqual(len(distrib._listeners), 0)
