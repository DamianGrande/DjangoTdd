import unittest

from selenium.webdriver.common.keys import Keys

from end_to_end_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                                               "You can't have an empty list item"))

        self.browser.find_element_by_id('id_new_item').send_keys('Buy rope for hang myself.')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy rope for hang myself.')

        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                                               "You can't have an empty list item"))

        self.browser.find_element_by_id('id_new_item').send_keys('Call a hooker.')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy rope for hang myself.')
        self.wait_for_row_in_list_table('2: Call a hooker.')


if __name__ == '__main__':
    unittest.main()
