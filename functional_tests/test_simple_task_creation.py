from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SMARKETS_EVENT_ADDRESS_SAMPLE = ('https://smarkets.com/event/957182/sport/'
                                 'football/league-cup/2018/09/25/'
                                 'wolverhampton-vs-leicester')


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):

        # Louise has heard about a new locally hosted
        # future betting app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention
        # future optional betting
        self.assertIn('Future Optional Betting', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('future optional bets', header_text)

        # She is invited to enter a smarkets web address
        inputbox = self.get_address_input_box()
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
        self.wait_for_cell_in_list_table('fc-barcelona-vs-girona-fc')

        table = self.browser.find_element_by_id(
            'id_matches_table')
        rows = table.find_elements_by_tag_name('tr')
        cells = []
        for row in rows:
            cells.extend(row.find_elements_by_tag_name('td'))
        self.assertTrue(any(cell.text == 'fc-barcelona-vs-girona-fc'
                            for cell in cells),
                        f"Football match did not appear in table, "
                        f"contents were:\n{table.text}"
                        )

        # There is still a text box inviting Louise
        # to add another item.
        # She enters:
        # https://smarkets.com/event/957182/sport/football/league-cup/
        # 2018/09/25/wolverhampton-vs-leicester
        inputbox = self.get_address_input_box()
        inputbox.send_keys('https://smarkets.com/event/957182/sport/'
                           'football/league-cup/2018/09/25/'
                           'wolverhampton-vs-leicester')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_cell_in_list_table('wolverhampton-vs-leicester')
        self.wait_for_cell_in_list_table('fc-barcelona-vs-girona-fc')

        # The page updates again,
        # and now shows both items on her list.
        self.check_for_cell_in_list_table('fc-barcelona-vs-girona-fc')
        self.check_for_cell_in_list_table('wolverhampton-vs-leicester')

    def test_user_has_future_bet_selection_options(self):
        # User comes to the site and enters a smarkets web address
        self.browser.get(self.live_server_url)
        inputbox = self.get_address_input_box()
        inputbox.send_keys(SMARKETS_EVENT_ADDRESS_SAMPLE)
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_cell_in_list_table('wolverhampton-vs-leicester')
        # User then sees options for 2-0, 2-2 home bet or 0-2, 2-2 away bet

        # User also sees an input box to enter an amount
        # with the text Amount already bet for each option
        home_input_box = self.get_amount_already_bet_home(
            SMARKETS_EVENT_ADDRESS_SAMPLE)
        self.assertEqual(home_input_box.get_attribute('placeholder'),
                         'Home: Amount already bet'
                         )
        away_input_box = self.get_amount_already_bet_away()
        self.assertEqual(away_input_box.get_attribute('placeholder'),
                         'Away: Amount already bet'
                         )

        # And another userbox with the price already bet
        home_price_already_bet_input_box = self.get_price_already_bet_home()
        self.assertEqual(
            home_price_already_bet_input_box.get_attribute('placeholder'),
            'Home price already bet'
        )
        away_price_already_bet_input_box = self.get_price_already_bet_away()
        self.assertEqual(
            away_price_already_bet_input_box.get_attribute('placeholder'),
            'Away price already bet'
        )
        # And another input box with the Text minimimum odds for each
        home_min_odds_input_box = self.get_min_price_to_bet_home()
        self.assertEqual(
            home_min_odds_input_box.get_attribute('placeholder'),
            'Home min odds'
        )
        away_min_odds_input_box = self.get_min_price_to_bet_away()
        self.assertEqual(
            away_min_odds_input_box.get_attribute('placeholder'),
            "Away min odds"
        )

        self.fail("Finish the Test")

    def test_multiple_users_can_start_tasks_at_different_urls(self):
        # Louise starts a new task
        self.browser.get(self.live_server_url)
        inputbox = self.get_address_input_box()
        inputbox.send_keys(
            'https://smarkets.com/event/958302/'
            'sport/football/premier-league/2018/09/29/'
            'man-city-vs-brighton')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_cell_in_list_table('man-city-vs-brighton')

        # She notices that her task has a unique URL
        louise_list_url = self.browser.current_url
        self.assertRegex(louise_list_url, '/tasks/.+')

        # Now a new user, Paul, comes along to the site

        # -- We use a new browser session to make sure
        # -- that no information of Louise's is coming
        # -- through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Peter visits the home page.  There is no sign of
        # Louise's task.

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('man-city-vs-brighton', page_text)
        self.assertNotIn('fc-barcelona-vs-girona-fc', page_text)
        self.assertNotIn('wolverhampton-vs-leicester', page_text)

        # Peter starts a new task by entering a new
        # smarkets event web address
        inputbox = self.get_address_input_box()
        inputbox.send_keys(
            'https://smarkets.com/event/958299/sport/'
            'football/premier-league/2018/09/29/'
            'arsenal-fc-vs-watford-fc')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_cell_in_list_table('arsenal-fc-vs-watford-fc')

        # Peter gets his own unique URL
        peter_list_url = self.browser.current_url
        self.assertRegex(peter_list_url, '/tasks/.+')
        self.assertNotEqual(peter_list_url, louise_list_url)

        # Again, there is no trace of Louise's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('man-city-vs-brighton', page_text)
        self.assertNotIn('fc-barcelona-vs-girona-fc', page_text)
        self.assertNotIn('wolverhampton-vs-leicester', page_text)

        # The website assumes that there has been
        # an amount bet on this event with the 2-0 refund offer

        # The website then presents Louise with various options
        # Score becomes 2-0, then 2-2,
        #self.fail('Finish the test!')
        # home_lead_then_comeback_text = self.browser.find_element_by_id(
        #    'home_lead_then_comeback_text')
        # home_lead_then_comeback_button =

    def test_website_displays_other_match_information(self):

        # The user goes to the website
        self.browser.get(self.live_server_url)

        # And enters in a smarkets event address
        inputbox = self.get_address_input_box()
        text_to_input = ('https://smarkets.com/event/956523/sport/football/'
                         'spain-la-liga/2018/09/23/fc-barcelona-vs-girona-fc')
        inputbox.send_keys(text_to_input)

        # When she hits enter, the page updates and now the page lists:
        # the name of this market
        # so that the Louise knows it's the right market.
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_cell_in_list_table('fc-barcelona-vs-girona-fc')

        # She also sees the date of the match
        # in a separate column in the list table
        table = self.browser.find_element_by_id(
            'id_matches_table')
        rows = table.find_elements_by_tag_name('tr')
        cells = []
        for row in rows:
            cells.extend(row.find_elements_by_tag_name('td'))
        self.assertIn('Sept. 23, 2018', [cell.text for cell in cells])

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
