import unittest
from slg.parameters import Parameters


class ParametersTestCase(unittest.TestCase):

    def setUp(self):
        self.parameters = Parameters()
        self.parameters.same = [
            'frequency',
            'age',
            'subjective_complexity',
            'familiarity'
        ]

    def test_parameters_calculate_alpha_method_returns_correct_result_without_differ_feature(self):
        self.parameters.differ = 'question'
        self.parameters.calculate_alpha()
        self.assertEqual(0.0125, self.parameters.alpha)

    def test_parameters_calculate_alpha_method_returns_correct_result_with_differ_feature(self):
        self.parameters.differ = 'syllables'
        self.parameters.calculate_alpha()
        self.assertEqual(0.01, self.parameters.alpha)

    # def test_calculator_returns_error_message_if_both_args_not_numbers(self):
    #     self.assertRaises(ValueError, self.calc.add, 'two', 'three')

if __name__ == '__main__':
    unittest.main()
