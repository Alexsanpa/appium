import unittest

from selenium.common.exceptions import NoSuchElementException

import os
from sapyautomation.web import find_elements
from sapyautomation.web.start_browser import Browser


class TestFindElements(unittest.TestCase):
    driver = None

    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')
        browser = Browser()
        self.driver = browser.start_browser('Firefox',
                                            'http://ussltcsnl1353.solutions'
                                            '.glbsnet.com:8000/sap/bc'
                                            '/ui5_ui5/ui2/ushell/shells'
                                            '/abap/FioriLaunchpad.html?sap'
                                            '-client=100#Shell-home')

    def test_find_element_by_id(self):
        element = find_elements.find_element_by_id(self.driver,
                                                   'USERNAME_FIELD'
                                                   '-inner')

        self.assertEqual(element != '', True)
        self.driver.close()

    def test_find_element_by_id_fail(self):
        self.assertRaises(NoSuchElementException,
                          find_elements.find_element_by_id, self.driver,
                          'USERNAME_FIELD-inne')
        self.driver.close()

    def test_find_element_by_name(self):
        element = find_elements.find_element_by_name(self.driver, 'sap-user')

        self.assertEqual(element != '', True)
        self.driver.close()

    def test_find_element_by_name_fail(self):
        self.assertRaises(NoSuchElementException,
                          find_elements.find_element_by_name, self.driver,
                          'sap-use')
        self.driver.close()

    def test_find_element_by_xpath(self):
        element = find_elements \
            .find_element_by_xpath(self.driver, "//input["
                                                "@id='USERNAME_FIELD-inner']")

        self.assertEqual(element != '', True)
        self.driver.close()

    def test_find_element_by_xpath_fail(self):
        self.assertRaises(NoSuchElementException,
                          find_elements.find_element_by_xpath, self.driver,
                          "//input[@id='USERNAME_FIELD-inne']")
        self.driver.close()

    def test_find_element_by_tag_name(self):
        element = find_elements \
            .find_element_by_tag_name(self.driver, "img")

        self.assertEqual(element != '', True)
        self.driver.close()

    def test_find_element_by_tag_name_fail(self):
        self.assertRaises(NoSuchElementException,
                          find_elements.find_element_by_tag_name, self.driver,
                          "im")
        self.driver.close()

    def test_find_element_by_class_name(self):
        element = find_elements \
            .find_element_by_class_name(self.driver, "sapMInputBaseInner")

        self.assertEqual(element != '', True)
        self.driver.close()

    def test_find_element_by_class_name_fail(self):
        self.assertRaises(NoSuchElementException,
                          find_elements.find_element_by_class_name,
                          self.driver,
                          "sapMInputBaseInne")
        self.driver.close()

    def test_find_elements_by_xpath(self):
        elements = find_elements \
            .find_all_elements_by_xpath(self.driver, "//div[contains(@class,"
                                                     "'sapUiSraBtnBlock')]")

        self.assertEqual(len(elements) > 0, True)
        self.driver.close()
