from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_task_matches(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_address_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(
                '.has-error').text,
            "You can't have an empty Smarkets event address"
        ))

        # She tries again with some text for the item, which now works
        self.get_address_input_box().send_keys(
            'https://smarkets.com/event/956523/sport/football/'
            'spain-la-liga/2018/09/23/fc-barcelona-vs-girona-fc')
        self.get_address_input_box().send_keys(Keys.ENTER)
        self.wait_for_cell_in_list_table('fc-barcelona-vs-girona-fc')
        # Perversely, she now decides to submit a second blank list item
        self.get_address_input_box().send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(
                '.has-error').text,
            "You can't have an empty Smarkets event address"
        ))

        # And she can correct it by filling some text in
        self.browser.find_element_by_id(
            'id_new_smarkets_event_address'
        ).send_keys(
            'https://smarkets.com/event/957182/sport/'
            'football/league-cup/2018/09/25/'
            'wolverhampton-vs-leicester')

        self.get_address_input_box().send_keys(
            Keys.ENTER)
        self.wait_for_cell_in_list_table('fc-barcelona-vs-girona-fc')
        self.wait_for_cell_in_list_table('wolverhampton-vs-leicester')
