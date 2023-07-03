import unittest
from lsverifier.analysis.analysis import get_prioritized_functions

class TestPrioritizedFunctions(unittest.TestCase):
    def test_get_prioritized_functions(self):
        c_file = 'main.c'
        expected_functions = ['ptr_func', 'vector_func', 'malloc_func', 'thread_func', 'bit_shift', 'main']

        function_list = get_prioritized_functions(c_file)

        self.assertEqual(function_list, expected_functions)

if __name__ == '__main__':
    unittest.main()