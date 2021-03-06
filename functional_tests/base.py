from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
import time

from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_cell_in_list_table(self, cell_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_matches_table')
                rows = table.find_elements_by_tag_name('tr')
                cells = []
                for row in rows:
                    cells.extend(row.find_elements_by_tag_name('td'))
                self.assertIn(cell_text, [cell.text for cell in cells])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
            time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
            time.sleep(0.5)

    def check_for_cell_in_list_table(self, cell_text):
        table = self.browser.find_element_by_id('id_matches_table')
        rows = table.find_elements_by_tag_name('tr')
        cells = []
        for row in rows:
            cells.extend(row.find_elements_by_tag_name('td'))
        self.assertIn(cell_text, [cell.text for cell in cells])

    def get_address_input_box(self):
        return self.browser.find_element_by_id('id_full_text')

    def get_amount_already_bet_home(self, div_id):
        # Some code here to get the div_id
        # Then some more code to get the element like below
        return self.browser.find_element_by_id('id_amount_already_bet_home')

    def get_amount_already_bet_away(self):
        return self.browser.find_element_by_id('id_amount_already_bet_away')

    def get_price_already_bet_home(self):
        return self.browser.find_element_by_id('id_price_already_bet_home')

    def get_price_already_bet_away(self):
        return self.browser.find_element_by_id('id_price_already_bet_away')

    def get_min_price_to_bet_home(self):
        return self.browser.find_element_by_id('id_min_price_to_bet_home')

    def get_min_price_to_bet_away(self):
        return self.browser.find_element_by_id('id_min_price_to_bet_away')