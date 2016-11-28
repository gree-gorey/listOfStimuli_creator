import unittest
from slg.store import Store


class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.store = Store()
        self.store.read_dummy_data_and_setup()

    def test_normalize_method_of_store(self):
        self.store.normalize()

        self.assertEqual(self.store.lists['list_1'][5].normalized_features['first'], 0.4)


if __name__ == '__main__':
    unittest.main()
