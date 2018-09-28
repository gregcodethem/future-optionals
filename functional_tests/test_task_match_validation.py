from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_task_matches(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty smarkets address. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_address_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # task page
        self.wait_for(lambda:
                      self.browser.find_element_by_css_selector(
                          '#id_text:invalid'
                      ))

        # She starts typing some text for the new match
        # and the error disappears
        self.get_address_input_box().send_keys(
            'https://smarkets.com/event/956523/sport/football/'
            'spain-la-liga/2018/09/23/fc-barcelona-vs-girona-fc')
        self.wait_for(lambda:
                      self.browser.find_element_by_css_selector(
                          '#id_text:valid'
                      ))

        # And she can submit it successfully
        self.get_address_input_box().send_keys(Keys.ENTER)
        self.wait_for_cell_in_list_table('fc-barcelona-vs-girona-fc')

        # Perversely, she now decides to submit a second blank list item
        self.get_address_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for_cell_in_list_table('fc-barcelona-vs-girona-fc')
        self.wait_for(lambda:
                      self.browser.find_element_by_css_selector(
                          '#id_text:invalid'
                      ))

        # And she can correct it by filling some text in
        self.get_address_input_box().send_keys(
            'https://smarkets.com/event/957182/sport/'
            'football/league-cup/2018/09/25/'
            'wolverhampton-vs-leicester')
        self.wait_for(lambda:
                      self.browser.find_element_by_css_selector(
                          '#id_text:valid'
                      ))
        self.get_address_input_box().send_keys(
            Keys.ENTER)
        self.wait_for_cell_in_list_table('fc-barcelona-vs-girona-fc')
        self.wait_for_cell_in_list_table('wolverhampton-vs-leicester')
