from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_matches_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_future_event_request_and_retrieve_it_later(self):

        # Louise has heard about a new locally hosted
        # future betting app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention
        # future optional betting
        self.assertIn('Future Optional Betting', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your future optional bets', header_text)

        # She is invited to enter a smarkets web address
        inputbox = self.browser.find_element_by_id(
            'id_new_smarkets_event_address')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a Smarkets event web address'
                         )

        # She writes in:
        # https://smarkets.com/event/956523/sport/
        # football/spain-la-liga/2018/09/23/fc-barcelona-vs-girona-fc
        text_to_input = ('https://smarkets.com/event/956523/sport/football/'
                         'spain-la-liga/2018/09/23/fc-barcelona-vs-girona-fc')
        inputbox.send_keys(text_to_input)

        # When she hits enter, the page updates and now the page lists:
        # the name of this market
        # so that the Louise knows it's the right market.
        inputbox.send_keys(Keys.ENTER)
        time.sleep(4)

        table = self.browser.find_element_by_id(
            'id_matches_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == 'fc-barcelona-vs-girona-fc'
                            for row in rows),
                        f"Football match did not appear in table, "
                        f"contents were:\n{table.text}"
                        )

        # There is still a text box inviting Louise
        # to add another item.
        # She enters:
        # https://smarkets.com/event/957182/sport/football/league-cup/
        # 2018/09/25/wolverhampton-vs-leicester
        inputbox = self.browser.find_element_by_id(
            'id_new_smarkets_event_address')
        inputbox.send_keys('https://smarkets.com/event/957182/sport/'
                           'football/league-cup/2018/09/25/'
                           'wolverhampton-vs-leicester')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        # The page updates again,
        # and now shows both items on her list.
        self.check_for_row_in_list_table('fc-barcelona-vs-girona-fc')
        self.check_for_row_in_list_table('wolverhampton-vs-leicester')

        # The website assumes that there has been
        # an amount bet on this event with the 2-0 refund offer

        # The website then presents Louise with various options
        # Score becomes 2-0, then 2-2,
        self.fail('Finish the test!')
        home_lead_then_comeback_text = self.browser.find_element_by_id(
            'home_lead_then_comeback_text')
        # home_lead_then_comeback_button =

        # --- Check with client if they want this to be
        # --- how much to bet
        # --- or total winnings/liability etc
        # and how much they want to bet (and price?) and on
        # which outcome : home/draw/away

        # Score becomes 0-2, then 2-2,
        # and how much they want to bet (and price?) and on
        # which outcome : home/draw/away

        # --- Other draw options can be introduced in the future
        # --- E.g. 2-0, then 3-3 etc
        # --- Time options can be introduced in the future
        # --- I.e. How many minutes are left and what to bet
        # The website will provide a minimum price option

        # The website will calculate how much should be placed.

        # The local website then displays
        # what options have been selected.

        # A scraping event is then set up behind the scenes
        # to update the score

        # When certain conditions are met with the score
        # a bet is then made as prescribed.
        # Placed with smarkets

        # Satisfied, she goes back to sleep
