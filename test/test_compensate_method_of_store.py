import unittest
from slg.store import Store, mean


class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.store = Store()
        self.store.read_dummy_data_and_setup()
        self.store.normalize()

        self.store.list_outputs['list_1'] = self.store.lists['list_1'][:2:]
        self.store.lists['list_1'] = self.store.lists['list_1'][2::]

        self.store.list_outputs['list_2'] = self.store.lists['list_2'][4::]
        self.store.lists['list_2'] = self.store.lists['list_2'][:4:]

    def test_compensate_method_of_store(self):
        initial_first_list_mean = self.store.list_mean['list_1'] = mean([word.normalized_features['first'] for word in self.store.list_outputs['list_1']])
        initial_second_list_mean = self.store.list_mean['list_2'] = mean([word.normalized_features['first'] for word in self.store.list_outputs['list_2']])
        self.store.compensate('first')

        now_first_list_mean = mean([word.normalized_features['first'] for word in self.store.list_outputs['list_1']])
        now_second_list_mean = mean([word.normalized_features['first'] for word in self.store.list_outputs['list_2']])

        self.assertTrue((initial_first_list_mean < now_first_list_mean) & (initial_second_list_mean > now_second_list_mean))


if __name__ == '__main__':
    unittest.main()
