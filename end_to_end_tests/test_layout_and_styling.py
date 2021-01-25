from selenium.webdriver.common.keys import Keys

from end_to_end_tests.base import FunctionalTest


class LayoutAndStyling(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)

        input_box.send_keys('Test.')
        input_box.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table('1: Test.')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)
