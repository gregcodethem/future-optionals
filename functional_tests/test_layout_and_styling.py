from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

SMARKETS_EVENT_ADDRESS_BASE = ('https://smarkets.com/event/956523/'
                               'sport/football/spain-la-liga/2018/09/23/')


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id(
            'id_new_smarkets_event_address')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys(SMARKETS_EVENT_ADDRESS_BASE + 'testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_cell_in_list_table('testing')
        inputbox = self.browser.find_element_by_id(
            'id_new_smarkets_event_address')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
