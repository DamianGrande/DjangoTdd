from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def _wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        input_box.send_keys('Start playing Metal Gear Solid.')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        input_box.send_keys('Lose weight (for real this time, I swear).')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        self._wait_for_row_in_list_table('1: Start playing Metal Gear Solid.')
        self._wait_for_row_in_list_table('2: Lose weight (for real this time, I swear).')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Clean the bathroom.')
        input_box.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table('1: Clean the bathroom.')

        url_user_1 = self.browser.current_url
        self.assertRegex(url_user_1, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Clean the bathroom.', page_text)
        self.assertNotIn('Start playing Metal Gear Solid.', page_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Looking for a new job without pairing.')
        input_box.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table('1: Looking for a new job without pairing.')

        url_user_2 = self.browser.current_url
        self.assertRegex(url_user_2, '/lists/.+')

        self.assertNotEqual(url_user_1, url_user_2)

        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Clean the bathroom', page_text)
        self.assertIn('Looking for a new job without pairing.', page_text)

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


if __name__ == '__main__':
    unittest.main()
