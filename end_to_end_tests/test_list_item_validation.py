import unittest

from end_to_end_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.fail('Test incomplete')


if __name__ == '__main__':
    unittest.main()
