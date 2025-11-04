import unittest

import os
from sapyautomation.desktop.process import is_chrome_running, \
    is_firefox_running
from time import sleep
from sapyautomation.web.start_browser import Browser


class TestStartBrowser(unittest.TestCase):

    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

    def test_start_browser_firefox(self):
        browser = Browser('Firefox')
        driver = browser.start_browser('http://ussltcsnl1353.solutions'
                                       '.glbsnet.com:8000/sap/bc'
                                       '/ui5_ui5/ui2/ushell/shells'
                                       '/abap/FioriLaunchpad.html?sap'
                                       '-client=100#Shell-home')
        self.assertEqual(driver != '', True)

    def test_start_browser_chrome(self):
        browser = Browser('Chrome')
        driver = browser.start_browser('http://ussltcsnl1353.solutions'
                                       '.glbsnet.com:8000/sap/bc'
                                       '/ui5_ui5/ui2/ushell/shells'
                                       '/abap/FioriLaunchpad.html?sap'
                                       '-client=100#Shell-home')
        self.assertEqual(driver != '', True)

    def test_close_browser_chrome(self):
        browser = Browser('Chrome')
        browser.start_browser('http://ussltcsnl1353.solutions'
                              '.glbsnet.com:8000/sap/bc'
                              '/ui5_ui5/ui2/ushell/shells'
                              '/abap/FioriLaunchpad.html?sap'
                              '-client=100#Shell-home')

        browser.close_browser()
        sleep(2)
        self.assertEqual(is_chrome_running(), False)

    def test_close_browser_firefox(self):
        browser = Browser('Firefox')
        browser.start_browser('http://ussltcsnl1353.solutions'
                              '.glbsnet.com:8000/sap/bc'
                              '/ui5_ui5/ui2/ushell/shells'
                              '/abap/FioriLaunchpad.html?sap'
                              '-client=100#Shell-home')

        browser.close_browser()
        self.assertEqual(is_firefox_running(), False)
