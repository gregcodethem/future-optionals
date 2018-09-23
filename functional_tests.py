from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_future_event_request_and_retrieve_it_later(self):

        # Louise has heard about a new locally hosted
        # future betting app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention
        # future optional betting
        self.assertIn('Future Optional Betting', self.browser.title)

        self.fail('Finish the test!')

        # She is invited to enter a betfair event code

        # The website then displays the name of this market
        # so that the Louise knows it's the right market.

        # The website assumes that there has been
        # an amount bet on this event with the 2-0 refund offer

        # The website then presents Louise with various options
        # Score becomes 2-0, then 2-2,
        # --- Check with client if they want this to be
        # --- how much to bet
        # --- or total winnings/liability etc
        # and how much they want to bet (and price?)

        # Score becomes 0-2, then 2-2,

        # --- Other draw options can be introduced in the future
        # --- E.g. 2-0, then 3-3 etc
        # --- Time options can be introduced in the future
        # --- I.e. How many minutes are left and what to bet

        # The local website then displays
        # what options have been selected.

        # A scraping event is then set up behind the scenes
        # to update the score

        # When certain conditions are met with the score
        # a bet is then made as prescribed.

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main()
