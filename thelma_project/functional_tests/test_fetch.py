# import pytest # Do Not Need This - pytest is intended runner though.
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


class TestFetchFunctionality(LiveServerTestCase):

    def setUp(self):

        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):

        self.browser.quit()

    def test_smoke_test(self):

        self.assertEqual(1, 1)

    def test_user_can_fetch_mnemonic_range(self):

        # Navigate to the fetch sub-application
        self.browser.get('http://localhost:1234')

        # User locates the input boxes in the application
        mnemonic_input = self.browser.find_element_by_id('mnemonic')
        self.assertEqual(
            mnemonic_input.get_attribute('placeholder'),
            'Enter a mnemoic'
        )

        start_doy_input = self.browser.find_element_by_id('startOfRangeInput')
        self.assertEqual(
            start_doy_input.get_attribute('placeholder'),
            'Start YYYY:DOY'
        )
        end_doy_input = self.browser.find_element_by_id('endOfRangeInput')
        self.assertEqual(
            end_doy_input.get_attribute('placeholder'),
            'End YYYY:DOY'
        )

        # # Next the user enters the fetch parameters into the inputs
        mnemonic_input.send_keys('DK_GENERATED')
        start_doy_input.send_keys('2019:001:00:00:00.000')
        end_doy_input.send_keys('2020:001:00:00:00.000')

        # # Then the user locates the fetch button
        fetch_button = self.browser.find_element_by_id('submit')
        fetch_button.click()
